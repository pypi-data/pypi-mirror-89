#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import shutil
import csv
import argparse

#import logging
#logging.basicConfig()
#logger = logging.getLogger()

from joblib import Parallel, delayed

from texsurgery.texsurgery import TexSurgery
#from pyexams.metadata_collector import MetadataCollector

class Exams(object):
    """Exams is the main class for reading a source tex file and then
    - reading all metadata and storing it into the database
    - exporting the questions in pdf or moodle format
    - grading the pdf forms
    - sending the statements, or solutions, or commented exams to the students
    - this list will probably grow
    """

    def __init__(self, tex_path):
        self.path = tex_path
        with open(tex_path, 'r') as tex_file:
            self.src = tex_file.read()
        self.ts = TexSurgery(self.src)
        #self.exercise_list is a lazy property
        self._exercise_list = None

    @property
    def exercise_list(self):
        if not self._exercise_list:
            self._exercise_list = dict()
            self.ts.findall('question[_nargs=1],questionmult[_nargs=1],questionmultx[_nargs=1]')
        return self._exercise_list

    def _try_command(self, command):
        process = subprocess.Popen(command, bufsize=-1,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        exit_code = process.returncode
        if exit_code:
            print('-'*10)
            print(stdoutdata)
            print('-'*10)
            print(stderrdata)
            print('-'*10)
            sys.exit(exit_code)

    def to_moodle(self, n):
        tex_source, tex_path = self.src, self.path
        basename = os.path.splitext(tex_path)[0]
        tmp_base_path = '%s_moodle_tmp'%(basename)
        tmp_path = tmp_base_path + '.tex'

        file = open('students.csv', 'r')
        student_list = list(csv.reader(file, skipinitialspace=True))
        field_names = student_list[0]
        extra_fields = field_names[4:]
        # These variables are only used in the pdf, they do not get exported into moodle
        # (unless the author includes them within the exercises, which she shouldn't)
        dummy = dict(
            name='name', surname='surname',
            include_solution='include_solution')
        dummy.update(dict(zip(extra_fields, extra_fields)))
        exercises = self.exercise_list

#        for j in range(n):
            # This one has to be different!
        dummy['seed'] = dummy['index'] = '123'
        ts = self.ts
        ts.data_surgery(dummy).code_surgery()
        tex_out = ts.src
        del ts
        # Call pdflatex
        with open(tmp_path, 'w') as tmp_file:
            tmp_file.write(tex_out)
        self._try_command( ['amc2moodle', tmp_path])
        # Read -moodle.xml

            # Collect exercise data from xml

        # Assemble the final xml file

    def to_pdf(self, with_statement, with_solution, do_all):
        tex_source, tex_path = self.src, self.path
        basename = os.path.splitext(tex_path)[0]

        stytemplate = r'''\newif\ifsolution
    \solution%(include_solution)s
    \def\name{\unexpanded{%(name)s}}
    \def\surname{\unexpanded{%(surname)s}}
    \def\seed{%(student_seed)s}
        '''
        TYPES = []
        if with_statement:
#            statements_file = open('email_list_statements', 'w')
            statements_file = None
            TYPES.append(('question', 'false', statements_file))
        if with_solution:
#            solutions_file = open('email_list_solutions', 'w')
            solutions_file = None
            TYPES.append(('solution', 'true', solutions_file))
        if do_all:
            for path,_,_ in TYPES:
                if os.path.exists(path):
                    shutil.rmtree(path)
                os.mkdir(path)
        # TODO clean data file
    #    data_file = basename + '.data'
    #    if do_all and os.path.exists(data_file):
    #        os.remove(data_file)

        file = open('students.csv', 'r')
        student_list = list(csv.reader(file, skipinitialspace=True))
        field_names = student_list[0]
        extra_fields = field_names[4:]

#        TYPES = [('question', 'false', None)]

        def one_pdf(student, index=0):
            name,surname,id,email,*extra_vals = student
            tmp_base_path = '%s_%s_tmp'%(basename,id)
            tmp_path = tmp_base_path + '.tex'
            pdf_tmp_path = '%s_%s_tmp.pdf'%(basename,id)
            pdf_output_file = basename + '.pdf'
            student_seed = id
            for (type, include_solution, output_file) in TYPES:
                student_vars = dict(
                    name=name, surname=surname, id=id, seed=id, index=index,
                    include_solution=include_solution)
                student_vars.update(dict(zip(extra_fields, extra_vals)))
                #TODO: add import to load our own sty instead of automultiplechoice
                ts = TexSurgery(self.src)
                ts.data_surgery(student_vars).code_surgery()
                #TODO: collect exam information
                tex_out = ts.src
                del ts
                with open(tmp_path, 'w') as tmp_file:
                    tmp_file.write(tex_out)
                self._try_command( ['pdflatex', '-halt-on-error', '-output-directory', '.', tmp_path])
                if do_all:
                    pdf_destination = '%s/%s_%s.pdf'%(type, type, id)
                    os.rename(pdf_tmp_path, pdf_destination)
                    #TODO: collect student data with joblib
    #                output_file.write(','.join([email, pdf_destination])+'\n')
                else:
                    if os.path.exists(pdf_output_file):
                        os.remove(pdf_output_file)
                    os.rename(pdf_tmp_path, pdf_output_file)
                for ext in ('.tex', '.log', '.aux', '.amc'):
                    if os.path.exists(tmp_base_path + ext):
                        os.remove(tmp_base_path + ext)

        if do_all:
            student_list_to_process = student_list[1:]
            Parallel(n_jobs=8)(delayed(one_pdf)(student, j)
                for j,student in enumerate(student_list_to_process))
        else:
            one_pdf(student_list[1])
        # Non-parallel version
        # for student in student_list_to_process:
        #     one_pdf(student)

    #    for _,_,file in TYPES:
    #        file.close()
