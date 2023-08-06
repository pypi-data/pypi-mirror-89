from __future__ import print_function

from Bio import Entrez
import pandas as pd
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import subprocess
import os
import argparse
import sqlite3


## other programs #########################################
def getMatch(term, alist):
    """
    This program internally used in ncbi_getTaxonomy and ncbi_Sp2Taxa

    term: search_string
    """

    pattern = re.compile(term)
    matching_list = [i.split('__')[1] for i in alist if pattern.match(i)]

    if len(matching_list) == 0:
        return ''
    else:
        return matching_list[0]

def TaxaRankingFormat(rank_levels, rank_names, levels_n = 7, style='regular'):
    """
    This program is internally used to format taxonomy xml retrieved from ncbi into ranking

    rank_levels: a list containing ranking ['kingdom',...]
    rank_names: a list containing name in the rank ['Abes', ....]

    style: regular: kingdom__[];class__[];
            qiime: D_0__[];D_1__[];
    level_n: how many taxonomy levels to get,default 7; 
            0: all levels;


    return a string
    """

    combined = ';'.join(list(map(lambda x: '__'.join(x), list(zip(rank_levels, rank_names)))))

    rankings = combined.split(';')
    taxa = None

    if levels_n == 7:

        if style == 'regular':
            # kingdom:
            kingdom = 'k__' + getMatch('^kingdom__', rankings)
            phylum = 'p__' + getMatch('^phylum__', rankings)
            classes = 'c__' + getMatch('^class__', rankings)
            order = 'o__' + getMatch('^order__', rankings)
            family = 'f__' + getMatch('^family__', rankings)
            genus = 'g__' + getMatch('^genus__', rankings)
            species = 's__' + getMatch('^species__', rankings)

            taxa = ';'.join([kingdom, phylum, classes, order, family, genus, species])

        elif style == 'qiime':

            kingdom = 'D_0__' + getMatch('^kingdom__', rankings)
            phylum = 'D_1__' + getMatch('^phylum__', rankings)
            classes = 'D_2__' + getMatch('^class__', rankings)
            order = 'D_3__' + getMatch('^order__', rankings)
            family = 'D_4__' + getMatch('^family__', rankings)
            genus = 'D_5__' + getMatch('^genus__', rankings)
            species = 'D_6__' + getMatch('^species__', rankings)

            taxa = ';'.join([kingdom, phylum, classes, order, family, genus, species])
        else:
            print('Style has to be regular or qiime.Please check the parameter')
            return

    elif levels_n == 0:
        link_ranks = []
        for i in range(len(rankings)):
            prefix = 'D_'+str(i)+'_'
            terms = prefix+'-'.join(rankings[i].split())
            link_ranks.append(terms)

        taxa = ';'.join(link_ranks)

    else:
        print('levels_n has to be 7 or 0. Please check the parameter.\n')
        return

    return taxa



#####################################################################



class LoadSpecies:

    def __init__(self, species_input, species_output, ifout = True):
        """
        species_input: file name containing the species information
        dtype: file type: csv, excel, table or fasta
        """
        self.species_input = species_input
        self.out_sp = species_output
        self.ifout = ifout

    def ReadSpeciesFile_text(self):

        sp_list = []
        with open(self.species_input, 'r') as input_list:
            for line in input_list:
                line = line.strip()
                sp_list.append(line)

        if self.ifout:
            with open(self.species_input, 'w') as outfile:
                for i in sp_list:
                    print(i, sep='', file=outfile)

        return sp_list



    def ReadSpeciesFile_excel(self, sp_col='act_sym_fullname', sheetname = 0, header = 0,  fullname = False):
        """
        sp_col: column that contains species
        """

        load_sp = pd.read_excel(self.species_input, sheet_name = sheetname, header=header) # use all column
        # extract the column
        sp = load_sp[sp_col]

        if fullname:
            sp_names = sp
            if self.ifout:
                sp_names.to_csv(self.out_sp, index=False)
        else:
            sp_names = sp.apply(lambda x: ' '.join(x.split()[0:2]))
            if self.ifout:
                sp_names.to_csv(self.out_sp, index=False)


        return list(sp_names)

    def ReadSpeciesFile_csv(self, sp_col='act_sym_fullname', header = 0, fullname = False):

        load_sp = pd.read_csv(self.species_input, header=header)
        # extract the column
        sp = load_sp[sp_col]

        if fullname:
            sp_names = sp
            if self.ifout:
                sp_names.to_csv(self.out_sp, index = False)

        else:
            sp_names = sp.apply(lambda x: ' '.join(x.split()[0:2]))
            if self.ifout:
                sp_names.to_csv(self.out_sp, index = False)

        return list(sp_names)

    def ExtractSpeciesFromFasta(self, ranges, delimiter = ' '):
        """
        ranges: a list
        seps: a list of delimiters
        """

        sp_names = []
        with open(self.species_input, 'r') as fna:
            for line in fna:
                line = line.strip()
                if line.startswith('>'):
                    header = line.split('>')[1]
                    spes = header.split(delimiter)[ranges]
                    sp_names.append(spes)

        if self.ifout:
            with open(self.out_sp, 'w') as out:
                for i in sp_names:
                    print(i, sep = '', file = out)

        return sp_names

    # def GetIdFromFasta(self):
    #     """
    #     Standard, fasta
    #     """
    #     with open(self.species_input, 'r') as fna:


class NCBI_Tools:
    def __init__(self, key, email, sqlite_db, ncbi_db, idtype):
        self._key = key # non-public
        self._email = email # non-public
        self.sqlite_db = sqlite_db
        self.ncbi_db = ncbi_db
        self.idtype = idtype
        self.track = []

    def __str__(self):
        output = ';'.join(self.track)
        return output

    def Update_API(self, key, email):
        self._key = key
        self._email = email

    def getTracker(self):
        tracked = self.track
        return tracked

    def ncbi_Species2Genome(self,sp_list):
        """
        This function assists to retrieve genome information.
        ID: species ID. must be a list.
        """
        print(
        """
        #########################################################\n
        ############ Convert Species list to Acc ID #############\n
        #########################################################\n
        """)
        Entrez.api_key = self._key 
        Entrez.email = self._email


        def getCore_ID(xml_root):
            ID = []
            for child in root:
                for i in child.find('LinkSetDb'):
                    for child_2 in i:
                        ID.append(child_2.text)

            return ID


        if type(sp_list) != list:
            print('ID input must be a list.')
            print('Exiting Run')
            return

        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return

        # create the database
        cur.execute('''CREATE TABLE IF NOT EXISTS Sp2Genome (rowid INT PRIMARY KEY, species TEXT, genome_id TEXT, acc_id TEXT)''')
        conn.commit()
        # species check if there is a hit in genome
        # check if existed
        cur.execute('''SELECT species FROM sp2genome''')
        getAll = cur.fetchall()
        n = len(getAll)
        if n > 0:
            existed_sp = [i[0] for i in getAll]
        else:
            existed_sp = []

        print('Existed {} Species Genome in the database'.format(len(getAll)))
        row_n = n

        acc_ID = []
        for i in range(len(getAll), len(sp_list)):
            # search
            current_sp = sp_list[i]
            if current_sp in existed_sp:
                print("{} Existed in the database".format(current_sp))
            else:
                try:
                    search = Entrez.esearch(db='genome', term=current_sp)
                    record = Entrez.read(search) # get the list
                    ID_list = record['IdList']

                except:
                    print("Entrez Error. Please Check Input Format")

                if len(ID_list) == 0:
                    print("{}: {} Genome NOT FOUND!".format(row_n, current_sp))
                    acc_ID.append('NA')
                    cur.execute('''INSERT OR IGNORE INTO Sp2Genome VALUES (?, ?, ?, ?)''', (row_n, current_sp, 'NA', 'NA'))
                    conn.commit()
                    row_n += 1

                else:
                    # convert to nuccore id

                    link = Entrez.elink(db='nuccore', dbfrom = 'genome', id=ID_list[0])
                    link_xml = link.read()
                    root = ET.fromstring(link_xml)

                    core_id = getCore_ID(root)

                    for id_each in range(len(core_id)):
                        print('{} Converting {}'.format(row_n, current_sp))
                        acc_ID.append(core_id[id_each])
                        cur.execute('''INSERT OR IGNORE INTO Sp2Genome VALUES (?, ?, ?, ?)''', (row_n, current_sp, ID_list[0], core_id[id_each]))
                        conn.commit()
                        row_n += 1

        self.track.append('P9')           
                    
        return acc_ID


    def ncbi_Search2Acc(self, terms, howmany = 0):
        """
        This function is used search term to get accesion IDs. In situations such as knowning species name or gene name, or no accession id available

        howmany: 0 select all

        """

        # this function use to adjust the code for iter_num
        def retMax(n):
            if n >= 100000:
                return 100000 # maximum for entrez 100,000
            else:
                return n


        Entrez.api_key = self._key
        Entrez.email = self._email

        print(
        """
        #########################################################\n
        ############ NCBI search database to get Acc ############\n
        #########################################################\n
        """)

        # setup database
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)

        

        cur.execute('''CREATE TABLE IF NOT EXISTS Search2AccIDs ( rowid INT PRIMARY KEY, acc_id TEXT )''')
        cur.execute('''SELECT acc_id FROM Search2AccIDs''')
        all_acc = cur.fetchall()

        # flatten the tuple
        existed = len(all_acc)
        print("Existed {} in Database\n".format(existed))

        if existed > 0:
            all_acc_flat = [ i[0] for i in all_acc ]
        else:
            all_acc_flat = []

        total_count = None
        try:
            handle = Entrez.esearch(db=self.ncbi_db, term=terms)
            # get total records
            record = Entrez.read(handle)
            total_count = int(record['Count'])
            print('\nTotal Count Found on the search : {}\n'.format(total_count))
            handle.close()
        except:
            print("\nEntrez Error\n")


        if total_count == 0:
            print("No Record Found, Please check search terms.\n")
            return
        


        # howmany 0: all the terms
        # howmany > 100000: over 100000
        # howmany <= 100000: small than 100000
        

        remain = total_count - existed
        iter_num = remain
        n = existed
        rd = 1
        count = remain
        row_n = existed + 1

        if howmany == 0:
            
            print("\nSelect to retrieve all {} terms that can be found...\n".format(total_count))
            print("{} remained to fetch\n".format(remain))

            
            if remain > 100000:
                # bulk retrieve

                while iter_num > 0:

                    retM = retMax(iter_num) # max retrieve is 100,000

                    try:
                        handle = Entrez.esearch(db=self.ncbi_db, term=terms, retmax=retM, retstart=n, idtype = self.idtype)
                    except:
                        print("\nEntrez Error\n")

                    record = Entrez.read(handle)
                    handle.close() # close the handle if done
                    # generator object to save memory
                    record_generator = ( g for g in record['IdList'])
                    for i, item in enumerate(record_generator):
                        print('Saving to Database. Batch No. {}'.format(rd))
                        print("Remaining {}".format(count))
                        if item not in all_acc_flat:
                            print(i, ' ', item, ' ', 'Row Number: ', row_n)
                            cur.execute('''INSERT OR IGNORE INTO Search2AccIDs (rowid, acc_id) VALUES (?,?)''', (row_n, item))
                            conn.commit()
                            count -= 1
                            row_n += 1
                        else:
                            print("<Id exists in the database>\n")

                    iter_num -= retM
                    n += retM
                    rd += 1

                    time.sleep(1)


            elif remain >= 0 and remain <= 100000:
                try:
                    handle = Entrez.esearch(db=self.ncbi_db, term=terms, retmax=remain, retstart = existed, idtype = self.idtype)
                    record = Entrez.read(handle)
                    record_generator = (g for g in record['IdList'])
                except:
                    print("\nEntrez Error\n")
                handle.close()
                

                for k, item in enumerate(record_generator):
                    print('Saving to Database. Batch No. {}'.format(rd))
                    print("Remaining {}".format(count))
                    if item not in all_acc_flat:
                        print(k, ' ', item, ' ', 'Row Number: ', row_n)
                        cur.execute('''INSERT OR IGNORE INTO Search2AccIDs (rowid, acc_id) VALUES (?, ?)''', (row_n, item))
                        conn.commit()
                        count -= 1
                        row_n += 1
                    else:
                        print("<Id exists in the database>\n")



        elif howmany > 100000 and howmany < total_count:


            while iter_num > 0 :

                retM = retMax(iter_num)
                try:
                    handle = Entrez.esearch(db=self.ncbi_db, term=terms, retmax=retM, retstart=n, idtype = self.idtype)
                    record = Entrez.read(handle)
                    record_generator = ( g for g in record['IdList'] )
                except:
                    print("\nEntrez Error\n")


                handle.close()

                for j, item in enumerate(record_generator):
                    print('Saving into database. Batch {}'.format(rd))
                    if item not in all_acc_flat:
                        print(j, ' ', item, ' ', 'Row Number: ', row_n)
                        cur.execute('''INSERT OR IGNORE INTO Search2AccIDs (rowid, acc_id) VALUES (?, ?)''', (row_n, item))
                        conn.commit()
                        row_n += 1
                    else:
                        print("<Id exists in the database>\n")

                iter_num -= retM
                n += retM
                rd += 1

                time.sleep(1)


        elif howmany <= 10000 and howmany > 0:

            try:
                handle = Entrez.esearch(db=self.ncbi_db, term=terms, retmax=howmany, idtype = self.idtype)
                record = Entrez.read(handle)
            except:
                print("\nEntrez Error\n")
            handle.close()
            aList = record['IdList']

            for u in range(len(aList)):
                print(aList[i])
                item = aList[i]
                if item not in all_acc_flat:
                    print(u, ' ', item, ' ', 'Row Number: ', row_n)
                    cur.execute('''INSERT OR IGNORE INTO Search2AccIDs (rowid, acc_id) VALUES (?, ?)''', (row_n, item))
                    conn.commit()
                    row_n += 1
                else:
                    print("<Id exists in the database>\n")             


        print("\n")
        print("Checking Saved Database\n")

        cur.execute('''SELECT acc_id FROM Search2AccIDs''')
        final_count = len(cur.fetchall())
        cur.close()
        conn.close()
        print("\nTotal {}\tRetrieved {}\n".format(total_count, final_count))
        if final_count == total_count:
            print("Completed!")
        else:
            print("{} needs to retrieve\n".format(total_count - final_count))

        return self.track.append('P1')


##################################
    def ncbi_Species2Acc(self, species_list, *more_terms):
        """
        This is to use when you have a bunch of species names to be converted to accession IDs.

        s_db: search database. default: nuccore
        more_term: terms to add to s_term

        updated
        """

        print(
        """
        #########################################################\n
        ############ NCBI ncbi species to accession #############\n
        #########################################################\n
        """)

        Entrez.api_key = self._key
        Entrez.email = self._email

        if type(species_list) == str and species_list.endswith('.lst'):
            sp_names = []
            try:
                with open(species_list, 'r') as sp:
                    for i in sp:
                        i = i.strip()
                        sp_names.append(i)
            except ValueError:
                return "File Not Found"
        elif type(species_list) == list:
            sp_names = species_list

        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return

        cur.execute('''CREATE TABLE IF NOT EXISTS Sp2AccIDs (rowid INT PRIMARY KEY, species TEXT, acc_id TEXT)''')
        cur.execute('''SELECT species FROM Sp2AccIDs''') # check if species exists
        existed_species = cur.fetchall()

        len_existed_sp = len(existed_species)
        #flattern it
        print("[[Summary]]\nHave Extracted {} IDs".format(len_existed_sp))

        if len_existed_sp > 0:
            existed = [i[0] for i in existed_species]
        else:
            existed = []

        n = len_existed_sp
        for i in range(len_existed_sp, len(sp_names)):

            sp = sp_names[i]
            if sp in existed:
                print("{}: {} existed in the database".format(i, sp))
                continue
            
            else:
                search_term = ' AND '.join([sp+'[ORGN]', ' AND '.join(more_terms)])
                print('\n{} Search Term: {}'.format(i, search_term))

                # search total count for a specific term
                try:
                    handle = Entrez.esearch(db=self.ncbi_db, term = search_term)
                    total_record = int(Entrez.read(handle)['Count'])
                except:
                    print("Entrez Error")

                if total_record > 0:
                    try:
                        handle = Entrez.esearch(db=self.ncbi_db, term = search_term, retmax = total_record, idtype = self.idtype)
                        record = Entrez.read(handle)
                        IDs = record['IdList']
                    except:
                        print("Entrez Error")


                    handle.close()

                    print("Entrez retrieved {} Accession IDs in {} \n".format(total_record, sp))

                    for i in range(len(IDs)):
                        print('Saving into database')
                        print(i, ' ', IDs[i], '\n')
                        cur.execute('''INSERT OR IGNORE INTO Sp2AccIDs (rowid, species, acc_id) VALUES (?,?,?)''', (n, sp, IDs[i]))
                        conn.commit()
                        n += 1
                        

                elif total_record == 0:
                    print("Entrez retrieved {} Accession IDs in {}. NOT FOUND!\n".format(total_record, sp))
                    cur.execute('''INSERT OR IGNORE INTO Sp2AccIDs (rowid, species, acc_id) VALUES (?,?,?)''', (n, sp, 'NA'))
                    conn.commit()
                    n += 1
                    

            time.sleep(3)

        cur.close()
        conn.close()
        print("\nCompleted!\n")
        return self.track.append('P2')
##################################################
    def ncbi_eAcc2Seq(self, ID):
        """
        Use external accession ID (list) to get fasta sequences, uid can work too

        store them in a database
        """
        print(
        """
        #########################################################\n
        ############ Accession list to get seq      #############\n
        #########################################################\n
        """)

        Entrez.api_key = self._key
        Entrez.email = self._email

        if type(ID) != list:
            print('ID parameter should be a list\nExit program')
            return 

        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return

        #set up sqlite
        cur.execute('''CREATE TABLE IF NOT EXISTS Acc2Seq (rowid INT PRIMARY KEY, acc_id TEXT, seq_description TEXT, sequences TEXT)''')
        cur.execute('''SELECT acc_id FROM Acc2Seq''')
        existed = cur.fetchall()

        if len(existed) > 0:
            existed_id = [i[0] for i in existed]
        else:
            existed_id = []

        len_all_acc = len(ID)


        if len_all_acc > 0:

            all_acc_flat = ID

            print('\nTotal Accession Numbers: {}\n'.format(len(all_acc_flat)))
            n = len(existed_id)
            for i in range(len(existed_id), len_all_acc):

                current_id = all_acc_flat[i]

                if  current_id in existed_id:
                    print("{} existed in the database".format(current_id))
                    continue
                else:

                    #Total number of records from the input set to be retrieved, up to a maximum of 10,000. 
                    if current_id == 'NA':
                        cur.execute('''INSERT INTO Acc2Seq VALUES (?, ?,?,?)''', (n, current_id, 'NA', 'NA'))
                        n += 1
                    else:
                        try:
                            # one at a time
                            fetch = Entrez.efetch(db = self.ncbi_db, id = current_id, retmode = 'text', rettype = 'fasta')
                            outs = fetch.read()
                        except:
                            print("Entrez Error\n")


                        fetch.close()
                        fasta = outs.strip().split('\n')
                        header = fasta[0]
                        acc, descript = header.split()[0].replace('>', ''), ' '.join(header.split()[1:])
                        seqs = ''.join(fasta[1:])

                        print('Saving into database:')
                        print('{} Acc_ID: {}\n'.format(i+1, acc))
                        cur.execute('''INSERT INTO Acc2Seq VALUES (?,?,?,?)''', (n, current_id, descript, seqs))
                        conn.commit()
                        n += 1

                        time.sleep(3)
        else:
            print("No Accession ID in the Database. Please Check!")
            return

        cur.close()
        conn.close()
        print('\nCompleted!\n')
        return self.track.append('P5')

    def ncbi_GetSeqsFromAcc(self, table_name, column_name='acc_id'):
        """
        Use Accession ID to get fasta sequences

        """

        print(
        """
        #########################################################\n
        ############ NCBI ncbi accession to fasta   #############\n
        #########################################################\n
        """)

        Entrez.api_key = self._key
        Entrez.email = self._email


        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return

        #set up sqlite
        cur.execute('''CREATE TABLE IF NOT EXISTS Acc2Seq (rowid INT PRIMARY KEY, acc_id TEXT, seq_description TEXT, sequences TEXT)''')

        try:
            # select the field contain acc id
            cur.execute('''SELECT {} FROM {}'''.format(column_name, table_name))
            all_acc = cur.fetchall()
            len_all_acc = len(all_acc)
        except sqlite3.Error as e:
            print("Error. Reading {} error\n".format(table_name))
            print(e)
            return

        cur.execute('''SELECT acc_id FROM Acc2Seq''')
        existed = cur.fetchall()
        if len(existed) > 0:
            existed_id = [i[0] for i in existed]
        else:
            existed_id = []

        if len_all_acc > 0:

            all_acc_flat = [i[0] for i in all_acc]

            print('\nTotal Accession Numbers: {}\n'.format(len(all_acc_flat)))
            n = len(existed_id)
            for i in range(len(existed_id), len_all_acc):

                current_id = all_acc_flat[i]

                if  current_id in existed_id:
                    print("{} existed in the database".format(current_id))
                    continue
                else:

                    #Total number of records from the input set to be retrieved, up to a maximum of 10,000. 
                    if current_id == 'NA':
                        cur.execute('''INSERT INTO Acc2Seq VALUES (?,?,?,?)''', (n, current_id, 'NA', 'NA'))
                        conn.commit()
                        n += 1
                    else:
                        try:
                            fetch = Entrez.efetch(db = self.ncbi_db, id = current_id, retmode = 'text', rettype = 'fasta')
                            outs = fetch.read()
                        except:
                            print("Entrez Error")


                        fetch.close()
                        fasta = outs.strip().split('\n')

                        if len(fasta) > 1:

                            header = fasta[0]
                            acc, descript = header.split()[0].replace('>', ''), ' '.join(header.split()[1:])
                            seqs = ''.join(fasta[1:])

                            print('Saving into database:')
                            print('{} Acc_ID: {}\n'.format(i+1, acc))
                            cur.execute('''INSERT INTO Acc2Seq VALUES (?,?,?,?)''', (n, current_id, descript, seqs))
                            conn.commit()
                            n += 1
                            time.sleep(3)

                        else:
                            print('Empty sequences')
                            cur.execute('''INSERT INTO Acc2Seq VALUES (?,?,?,?)''', (n, current_id, "NA", "NA"))
                            conn.commit()
                            n += 1
                            time.sleep(3)
        else:
            print("No Accession ID in the Database. Please Check!")
            return

        cur.close()
        conn.close()
        print('\nCompleted!\n')
        return self.track.append('P3')


    def ncbi_eAcc2TaxID(self, IDs):
        """
        Retrieve taxid from external accession ID (list), not just acc id, uid can work too

        store them in a database
        """
        print(
        """
        #########################################################\n
        ############    external UID  to get tax ID            ###\n
        #########################################################\n
        """)
        Entrez.api_key = self._key
        Entrez.email = self._email

        if type(IDs) != list:
            print('ID parameter should be a list\nExit program')
            return

        if len(IDs) == 0:
            print("The list is empty, please check")
            print("Exit")
            return

        # make sql connectio
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return
        # create uid taxid table
        # have to consider NA
        cur.execute('''CREATE TABLE IF NOT EXISTS Uid2TaxIDs (
                        rowid INT PRIMARY KEY,
                        acc_id TEXT, 
                        tax_id TEXT )''')

        cur.execute('''SELECT acc_id FROM Uid2TaxIDs''')
        extracted_ids = cur.fetchall()

        len_extracted_ids = len(extracted_ids)
        print("[[Summary]]\nHave extracted {} IDs\n".format(len_extracted_ids))

        if len_extracted_ids > 0:
            print('.......Start From ID {}......\n'.format(len_extracted_ids))
            all_old_ids = [i[0] for i in extracted_ids]
        else:
            all_old_ids = []

        ID = IDs

        n = len_extracted_ids
        for i in range(len_extracted_ids, len(ID)):

            # making sure we don't have to go over all the ID list again, if ID list is the same
            current_id = ID[i]
            if current_id in all_old_ids:
                print("{}: {} existed.")
                continue

            else:
                if current_id == 'NA':
                    print("{}: {} NOT FOUND".format(i, current_id))
                    cur.execute('''INSERT OR IGNORE INTO Uid2TaxIDs (rowid, acc_id, tax_id) VALUES (?, ?, ?)''', (n, current_id, 'NA'))
                    conn.commit()
                    n += 1
                else:
                    print("{} Load ID: {}".format(i, current_id))
                    try:
                        fetch = Entrez.efetch(db=self.ncbi_db, id=current_id, retmode='xml', rettype = 'fasta')
                        outs = fetch.read()
                    except:
                        print('Entrez eFetch Error\n')
                    fetch.close()

                    soup = BeautifulSoup(outs, 'lxml')
                    for j in soup.find('tseq_taxid'):

                        print('Taxonomy ID: {}'.format(j))

                        print("Saving into Database\n")
                        cur.execute('''INSERT OR IGNORE INTO Uid2TaxIDs (rowid, acc_id, tax_id) VALUES (?, ?, ?)''', (n, current_id, j))
                        conn.commit()

                    n += 1

                time.sleep(3)


        cur.close()
        conn.close()

        return self.track.append('P6')

    def ncbi_GetTaxIdFromIDs(self, table_name, column_name='acc_id'):
        """
        table, column: the table and field where to get nuccore_ID
        return a sqlite database conatin nuccore_ID and tax_ID
        """

        print(
        """
        #########################################################\n
        ############  Get taxonomy IDs from Accession Or UID  ###\n
        #########################################################\n
        """)
        Entrez.api_key = self._key
        Entrez.email = self._email

        # make sql connectio
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)
            return


        # create uid taxid table
        # have to consider NA
        cur.execute('''CREATE TABLE IF NOT EXISTS Uid2TaxIDs (
                        rowid INT PRIMARY KEY,
                        acc_id TEXT, 
                        tax_id TEXT )''')

        cur.execute('''SELECT acc_id FROM Uid2TaxIDs''')
        extracted_ids = cur.fetchall()

        len_extracted_ids = len(extracted_ids)
        print("[[Summary]]\nHave extracted {} IDs\n".format(len_extracted_ids))

        if len_extracted_ids > 0:
            print('.......Start From ID {}......\n'.format(len_extracted_ids))
            all_old_ids = [i[0] for i in extracted_ids]
        else:
            all_old_ids = []

        cur.execute('''SELECT {} FROM {}'''.format(column_name, table_name))
        ID = [i[0] for i in cur.fetchall()]

        n = len_extracted_ids
        for i in range(len_extracted_ids, len(ID)):

            # making sure we don't have to go over all the ID list again, if ID list is the same
            current_id = ID[i]
            if current_id in all_old_ids:
                print("{}: {} existed.")
                continue

            else:
                if current_id == 'NA':
                    print('ID is NA')
                    cur.execute('INSERT INTO Uid2TaxIDs (rowid, acc_id, tax_id) VALUES (?, ?, ?)', (n, current_id, 'NA'))
                    conn.commit()
                    n += 1
                else:                  
                    print("{} Load ID: {}".format(i, current_id))
                    try:
                        fetch = Entrez.efetch(db=self.ncbi_db, id=current_id, retmode='xml', rettype = 'fasta')
                        outs = fetch.read()
                    except:
                        print('Entrez eFetch Error\n')
                    fetch.close()

                    soup = BeautifulSoup(outs, 'lxml')

                    if soup.find('tseq_taxid') is not None:

                        for j in soup.find('tseq_taxid'):

                            print('Taxonomy ID: {}'.format(j))
                            print("Saving into Database\n")
                            cur.execute('INSERT INTO Uid2TaxIDs (rowid, acc_id, tax_id) VALUES (?, ?, ?)', (n, current_id, j))
                            conn.commit()

                    else:
                        print("Taxonomy ID: Empty")
                        print("Saving into Database\n")
                        cur.execute('INSERT INTO Uid2TaxIDs (rowid, acc_id, tax_id) VALUES (?, ?, ?)', (n, current_id, 'NA'))
                        conn.commit()
                    
                    n += 1

                time.sleep(3)


        cur.close()
        conn.close()

        return self.track.append('P4')



    def ncbi_Species2Taxa(self, sp_list, style='regular', levels_n = 7):
        """
        This function works as: [species list] ------> [search NCBI taxonomy] -----> [fetch taxonomy by uid] --------> [construct taxonomy]
        
        sqlite_db table: sp2taxa
        sp_list: species list (no var.) has to be unique

        return a table in sqlite database containing species names, uid, Ranking
        """

        print(
        """
        #########################################################\n
        ############  Retrieving Taxa Rank from Species list  ###\n
        #########################################################\n
        """)

        Entrez.api_key = self._key
        Entrez.email = self._email

        if type(sp_list) == list:
            sp_list = sp_list
        else:
            print("Species list should be a list")
            return

        if len(sp_list) > 0:

            try:
                conn = sqlite3.connect(self.sqlite_db)
                cur = conn.cursor()
            except sqlite3.Error as e:
                print(e)


            # create table
            cur.execute('''CREATE TABLE IF NOT EXISTS Sp2Taxa (rowid INT PRIMARY KEY, species TEXT, tax_id TEXT, ranking TEXT)''')
            # existed species
            cur.execute('''SELECT species FROM Sp2Taxa''')
            sp2taxa = cur.fetchall()

            howmany = len(sp2taxa)

            if howmany > 0:
                existed_sp2taxa = [i[0] for i in sp2taxa]
            else:
                existed_sp2taxa = []

            n = howmany
            for i in range(howmany, len(sp_list)):
                current_species = sp_list[i]
                if current_species in existed_sp2taxa:
                    print("{}: {} existed in the database.".format(i, current_species))
                    continue

                else:
                    try:
                        print("{} Searching term {}".format(i, current_species))
                        search = Entrez.esearch(db='taxonomy', term=current_species.strip())
                    except:
                        print('Entrez Error\n')

                    content = Entrez.read(search)
                    search.close()
                    uid = content['IdList']

                    if len(uid) > 0:

                        the_id = uid[0]

                        try:
                            fetch = Entrez.efetch(db='taxonomy', id=the_id, retmode='xml')
                            xml = fetch.read()
                        except:
                            print("Entrez Efetch Error!\n")

                        fetch.close()

                        all_levels_rank = []
                        all_levels_name = []
                        root = ET.fromstring(xml)
                        for name in root.findall('Taxon/LineageEx/Taxon/ScientificName'):
                            all_levels_name.append(name.text)
                        for rank in root.findall('Taxon/LineageEx/Taxon/Rank'):
                            all_levels_rank.append(rank.text)
                        #add species:
                        for s in root.findall('Taxon/ScientificName'):
                            all_levels_name.append(s.text)
                        for r in root.findall('Taxon/Rank'):
                            all_levels_rank.append(r.text)
                        
                        taxa = TaxaRankingFormat(all_levels_rank, all_levels_name, style=style, levels_n= levels_n)
                        cur.execute('''INSERT OR IGNORE INTO Sp2Taxa (rowid, species, tax_id, Ranking) VALUES (?, ?, ?, ?)''', (n, current_species, the_id, taxa))
                        conn.commit()
                        n += 1


                    else:
                        the_id = 'NA'
                        taxa = 'NA'
                        cur.execute('''INSERT OR IGNORE INTO Sp2Taxa (rowid, species, tax_id, Ranking) VALUES (?, ?, ?, ?)''', (n, current_species, the_id, taxa))
                        conn.commit()
                        n += 1                      


        else:
            print("Species List is empty. Exit the program\n")
            return

        return self.track.append('P7')

    def ncbi_Id2Taxa(self, style='regular', levels_n = 7):
        """
        Get taxonomy ranking information from taxonomy id. suppose you know accession id
        return:
        A Database
        tab separated:
        accession_id tab k__xxxx;p__xxxx;

        if levels == 7: get 7 levels: kingdom, phylum, class, order, family, genus, species
        else return all levels

        if qiime_type = True:
        D_0__Bacteria;---->D_6__Cpiroplasma leptinotarsae

        """

        print(
        """
        #########################################################\n
        ############  Get taxonomy IDs ranking From ID     ######\n
        #########################################################\n
        """)

        Entrez.api_key = self._key
        Entrez.email = self._email

        # open sqlite connect
        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS TaxId2Ranking ( 
                rowid INT PRIMARY KEY,
                acc_id TEXT,
                tax_id TEXT,
                ranking TEXT) ''' )

        except sqlite3.Error as e:
            print(e)
            return

        try:
            cur.execute('''SELECT acc_id, tax_id FROM Uid2TaxIDs''')
            existed_ID_Uid2TaxID = cur.fetchall()
        except sqlite3.Error as e:
            print("Error: Reading From Table Uid2TaxIDs\n")
            print("Exit the program")
            return

        len_old_Id = len(existed_ID_Uid2TaxID)
        if len_old_Id > 0:

            all_old_nuccore = [i[0] for i in existed_ID_Uid2TaxID]
            all_old_taxId = [i[1] for i in existed_ID_Uid2TaxID]

        else:
            print("No accession and tax id Found in database table Uid2TaxIDs!\n")
            print("Exit the program")
            return

        cur.execute('''SELECT acc_id FROM TaxId2Ranking''')
        existed_core_TaxId2Ranking = cur.fetchall()

        len_new_core = len(existed_core_TaxId2Ranking)
        if  len_new_core > 0:
            all_new_core = [i[0] for i in existed_core_TaxId2Ranking]
        else:
            all_new_core = []

        n = len_new_core
        for i in range(len_new_core, len_old_Id):
            current_id = all_old_nuccore[i]

            if current_id in all_new_core:
                print("{}: {} existed in the database.".format(i, current_id))

            else:
                if current_id == 'NA':
                    print('{} Tax ID is NA'.format(n))
                    taxa = 'NA'
                    taxID = 'NA'
                    cur.execute('INSERT OR IGNORE INTO TaxId2Ranking (rowid, acc_id, tax_id, ranking) VALUES (?,?,?,?)', (n, current_id, taxID, taxa))
                    conn.commit()
                    n += 1
                else:
                    try:
                        # get the xml form of the fetch
                        print("{} Retrieve ID {} taxonomy ranking".format(i, current_id))
                        handle = Entrez.efetch(db='taxonomy', id = all_old_taxId[i], retmode = 'xml')
                        xml = handle.read()
                    except:
                        print("Entrez eFetch Error. Please check!\n")

                    # extract taxonomy ranks
                    all_levels_names = []
                    all_levels_rank = []
                    root = ET.fromstring(xml)
                    for name in root.findall('Taxon/LineageEx/Taxon/ScientificName'):
                        all_levels_names.append(name.text)
                    for rank in root.findall('Taxon/LineageEx/Taxon/Rank'):
                        all_levels_rank.append(rank.text)
                    #add species:
                    for s in root.findall('Taxon/ScientificName'):
                        all_levels_names.append(s.text)
                    for r in root.findall('Taxon/Rank'):
                        all_levels_rank.append(r.text)

                    taxa = TaxaRankingFormat(all_levels_rank, all_levels_names, style=style, levels_n=levels_n)

                    cur.execute('INSERT OR IGNORE INTO TaxId2Ranking (rowid, acc_id, tax_id, ranking) VALUES (?,?,?,?)', (n, current_id, all_old_taxId[i], taxa))
                    conn.commit()
                    n += 1
                        
            time.sleep(3)


        cur.close()
        conn.close()

        return self.track.append('P8')


#-------------------------------------------------------

class Sqlite_Dumps:
    
    def __init__(self, sqlite_db, output_prefix, tracker, header_type = 'acc'):
        self.sqlite_db = sqlite_db
        self.prefix = output_prefix
        self.prefix = output_prefix
        self.idtype = header_type
        self.track = tracker # a list

    def sqlite_dump(self):
        """

        GENERATE a fasta and a mapping file
        format:
        >ACC_ID\tranking

        output: output fasta name.
        by: table=field
        """

        try:
            conn = sqlite3.connect(self.sqlite_db)
            cur = conn.cursor()
        except sqlite3.Error as e:
            print(e)

        tracked = ';'.join(self.track)
        idtype = self.idtype

        output = self.prefix+'.fasta'

        print("Tracker Flag:")
        print('--->'.join(self.track))

        
        if tracked.startswith("P1") and tracked.endswith("P8"):

            # get nuccore id
            cur.execute('''SELECT acc_id, sequences FROM Acc2Seq''')
            seq_fetch = cur.fetchall()
            acc_id = [i[0] for i in seq_fetch if i[0] != 'NA']
            seqs = [i[1] for i in seq_fetch if i[1] != 'NA']

            # get taxid
            cur.execute('''SELECT tax_id, ranking FROM TaxId2Ranking''')
            rank_fetch = cur.fetchall()
            tax_id = [i[0] for i in rank_fetch if i[0] != 'NA']
            rankings = [i[1] for i in rank_fetch if i[1] != 'NA']

            if len(acc_id) == 0 and len(seqs) == 0 and len(tax_id) == 0 and len(rankings) == 0:
                print('Database: All element in Acc2Seq, TaxId2Ranking are NA')
                print('No dumping\nExit')
                return

            with open(output, 'w') as fasta:
                for i in range(len(seqs)):
                    print("{} Writing {} to fasta".format(i, acc_id[i]))
                    if idtype == 'acc':
                        print('>' + acc_id[i], rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'taxid':
                        print('>' + tax_id[i], rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'both':
                        print('>' + '|'.join([acc_id[i], tax_id[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)

            # mapping output
            mapping = output.replace('.fasta', '.mapping')
            with (open(mapping, 'w')) as maps:
                for i in range(len(rankings)):
                    print("{}: Writing {} to taxonomy mapping".format(i, acc_id[i]))
                    if idtype == 'acc':
                        print(acc_id[i], rankings[i], sep='\t', file = maps)
                    elif idtype == 'taxid':
                        print(tax_id[i], rankings[i], sep='\t', file = maps)
                    elif idtype == 'both':
                        print('|'.join([acc_id[i], tax_id[i]]), rankings[i], sep='\t', file = maps)


        elif tracked.startswith("P2") and tracked.endswith("P8") and ( "P7" not in tracked ):
            cur.execute('''SELECT species, acc_id FROM Sp2AccIDs''')
            getAll = cur.fetchall()
            getSpecies = [i[0] for i in getAll if i[1] != 'NA']
            acc_id = [i[1] for i in getAll if i[1] != 'NA'] # have NAs

            if len(getSpecies) == 0 and len(acc_id) == 0:
                print('All elments in Sp2AccIDs are empty')
                print("Exit")
                return

            cur.execute('''SELECT sequences FROM Acc2Seq''')
            seqs = [i[0] for i in cur.fetchall() if i[0] != 'NA' ]


            cur.execute('''SELECT tax_id, ranking FROM TaxId2Ranking''')
            getAll2 = cur.fetchall()
            tax_id = [i[0] for i in getAll2 if i[0] != 'NA']
            rankings = [i[1] for i in getAll2 if i[1] != 'NA']

            with open(output, 'w') as fasta:
                for i in range(len(getSpecies)):
                    print('{}: Writing {} to fasta'.format(i, getSpecies[i]))
                    if idtype == 'acc':
                        print('>' + '|'.join([acc_id[i], getSpecies[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'taxid':
                        print('>' + '|'.join([tax_id[i], getSpecies[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'both':
                        print('>' + '|'.join([acc_id[i], tax_id[i], getSpecies[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
            # mapping output
            mapping = output.replace('.fasta', '.mapping')
            with (open(mapping, 'w')) as maps:
                for i in range(len(rankings)):
                    print('{}: Writing {} to taxonomy mapping'.format(i, getSpecies[i]))
                    if idtype == 'acc':
                        print('|'.join([acc_id[i], getSpecies[i]]), rankings[i], sep='\t', file = maps)
                    elif idtype == 'taxid':
                        print('|'.join([tax_id[i], getSpecies[i]]), rankings[i], sep='\t', file = maps)
                    elif idtype == 'both':
                        print('|'.join([acc_id[i], tax_id[i], getSpecies[i]]), rankings[i], sep='\t', file = maps)
      
        elif (tracked.startswith("P2") and tracked.endswith("P7")) or tracked.startswith('P7') or tracked.startswith("P2;P7") or tracked.startswith("P7;P2"):
            
            cur.execute('''SELECT species, acc_id FROM Sp2AccIDs''')
            getAll = cur.fetchall()
            getSpecies = [i[0] for i in getAll if i[1] != 'NA']
            acc_id = [i[1] for i in getAll if i[1] != 'NA'] # have NAs

            if len(getSpecies) == 0 and len(acc_id) == 0:
                print('All elments in Sp2AccIDs are empty')
                print("Exit")
                return

            cur.execute('''SELECT sequences FROM Acc2Seq''')
            seqs = [i[0] for i in cur.fetchall() if i[0] != 'NA' ]

            cur.execute('''SELECT species, tax_id, ranking FROM Sp2Taxa''') # THIS IS UNIQUE
            getAll2 = cur.fetchall()
            species = [i[0] for i in getAll2 ]
            tax_id = [i[1] for i in getAll2 ]
            rankings = [i[2] for i in getAll2 ]
            species_map = {}
            for i in range(len(species)):
                species_map[species[i]] = [tax_id[i], rankings[i]]

            with open(output, 'w') as fasta:

                for i in range(len(getSpecies)):
                    print('{}: Writing {} to fasta'.format(i, getSpecies[i]))
                    taxID = species_map[getSpecies[i]][0]
                    ranks = species_map[getSpecies[i]][1]

                    if idtype == 'acc':
                        print('>' + '|'.join([acc_id[i], getSpecies[i]]), ranks, sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'taxid':
                        print('>' + '|'.join([taxID, getSpecies[i]]), ranks, sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'both':
                        print('>' + '|'.join([acc_id[i], taxID, getSpecies[i]]), ranks, sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)


            mapping = output.replace('.fasta', '.mapping')
            with (open(mapping, 'w')) as maps:

                for i in range(len(getSpecies)):
                    print('{}: Writing {} to taxonomy mapping'.format(i, getSpecies[i]))
                    taxID = species_map[getSpecies[i]][0]
                    ranks = species_map[getSpecies[i]][1]

                    if idtype == 'acc':
                        print('|'.join([acc_id[i], getSpecies[i]]), ranks, sep='\t', file = maps)
                    elif idtype == 'taxid':
                        print('|'.join([taxID, getSpecies[i]]), ranks, sep='\t', file = maps)
                    elif idtype == 'both':
                        print('|'.join([acc_id[i], taxID, getSpecies[i]]), ranks, sep='\t', file = maps)



        elif (tracked.startswith("P5") and tracked.endswith("P8")) or (tracked.startswith("P6") and tracked.endswith("P8")):
            cur.execute('''SELECT acc_id, sequences FROM Acc2Seq''')
            getAll = cur.fetchall()
            acc_id = [i[0] for i in getAll if i[0] != 'NA'] # unique
            seqs = [i[1] for i in getAll if i[0] !='NA']

            if len(acc_id) == 0 or len(seqs) == 0:
                print('All elment in Acc2Seq are empty')
                print('No dumping\nExit')
                return

            cur.execute('''SELECT tax_id, ranking FROM TaxId2Ranking''')
            getAll2 = cur.fetchall()
            tax_id = [i[0] for i in getAll2 if i[0] != 'NA']
            rankings = [i[1] for i in getAll2 if i[0] != 'NA']

            with open(output, 'w') as fasta:
                for i in range(len(acc_id)):
                    print('{}: Writing {} to fasta'.format(i, acc_id[i]))
                    if idtype == 'acc':
                        print('>' + acc_id[i], rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'taxid':
                        print('>' + tax_id[i], rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'both':
                        print('>' + '|'.join([acc_id[i], tax_id[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)                   


            # mapping output
            mapping = output.replace('.fasta', '.mapping')
            with (open(mapping, 'w')) as maps:
                for i in range(len(rankings)):
                    print('{}: Writing {} to taxonomy mapping'.format(i, acc_id[i]))
                    if idtype == 'acc':
                        print(acc_id[i], rankings[i], sep='\t', file = maps)
                    elif idtype == 'taxid':
                        print(tax_id[i], rankings[i], sep='\t', file = maps)
                    elif idtype == 'both':
                        print('|'.join([acc_id[i], tax_id[i]]), rankings[i], sep='\t', file = maps)

        elif tracked.startswith('P9') and tracked.endswith('P8'):
            # select species and genome id from Sp2Genome
            cur.execute('''SELECT species, genome_id FROM Sp2Genome''')
            getAll = cur.fetchall()

            if len(getAll) <= 0:
                print("Sp2Genome database is empty! Please Check")
                print("Exit")
                return
            else:
                species = [i[0] for i in getAll if i[1] !='NA'] # deal with NA
                genome_id = [i[1] for i in getAll if i[1] !='NA']

            if len(species) == 0 and len(genome_id) == 0:
                print("All Genome ID in Sp2Genome are empty")
                print("No dumping\nExit")
                return

            # select acc_id and tax_id and ranking from TaxId2Ranking
            cur.execute('''SELECT acc_id, tax_id,ranking FROM TaxId2Ranking''')
            getAll2 = cur.fetchall()
            if len(getAll2) <= 0:
                print("TaxId2Ranking database is empty! Please Check")
                print("Exit")
                return
            else:
                acc_id = [i[0] for i in getAll2 if i[0] !='NA'] 
                tax_id = [i[1] for i in getAll2 if i[0] !='NA']
                rankings = [i[2] for i in getAll2 if i[0] != 'NA']

            # select sequences
            cur.execute('''SELECT acc_id, sequences FROM Acc2Seq''')
            getAll3 = cur.fetchall()
            if len(getAll3) <= 0:
                print("Acc2Seq database is empty! Please Check")
                print("Exit")
                return
            else:
                acc_id = [i[0] for i in getAll3 if i[0] !='NA'] 
                seqs = [i[1] for i in getAll3 if i[0] !='NA']


            with open(output, 'w') as fasta:
                for i in range(len(species)):
                    print('{}:Writing {} to fasta'.format(i, species[i]))
                    if idtype == 'acc':
                        print('>' + '|'.join([acc_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'taxid':
                        print('>' + '|'.join([tax_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)
                    elif idtype == 'both':
                        print('>' + '|'.join([acc_id[i], tax_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = fasta)
                        print(seqs[i], sep='', file = fasta)


            mapping = output.replace('.fasta', '.mapping')
            with (open(mapping, 'w')) as maps:

                for i in range(len(species)):
                    print('{}:Writing {} to taxonomy mapping'.format(i, species[i]))
                    if idtype == 'acc':
                        print('|'.join([acc_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = maps)
                    elif idtype == 'taxid':
                        print('|'.join([tax_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = maps)
                    elif idtype == 'both':
                        print('|'.join([acc_id[i], tax_id[i], species[i], genome_id[i]]), rankings[i], sep='\t', file = maps)

        else:
            print('{} not followed the procedure, please check instruction'.format(tracked))

        print("Dumping Completed!")
        return         


