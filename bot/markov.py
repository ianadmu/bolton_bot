#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os.path
import re
import random
import traceback

from collections import defaultdict
from collections import deque


class Markov:
    maximum_length = 100
    words_that_end_in_periods = (
        "Mrs", "Mr", "Co", "M", "Dr", "Ms", "Sr", "St", "Rd", "Ave", "Mt",
        "Blvd", "Org", "Ltd", "..."
    )
    terminators = [".", "!", "?"]
    characters_to_remove = re.compile("[\n\"`\”—‘…�’\(\);]")
    phrase_to_remove = re.compile("BOOK .* ")
    quotes_on_the_outside_of_words = ("' | '|(?<!.)'")

    def __init__(self, length, msg_writer, file_list=None):
        self.msg_writer = msg_writer
        self.length = length
        self.processing_string = ""
        self.chain = defaultdict(list)

        if file_list is not None and len(file_list) > 0:
            for file_name in file_list:
                self.add_file(file_name)
        else:
            self.add_single_line("This is the default phrase.")

    def add_file(self, file_name):
        try:
            with open(os.path.join('./resources', file_name), 'r') as file:
                for line in file:
                    self.process_line(line)
            self.process_current_string()
        except:
            err_msg = traceback.format_exc()
            logging.error('Unexpected error: {}'.format(err_msg))
            self.msg_writer.write_error(err_msg)
            pass

    def add_single_line(self, line):
        line = re.sub(self.characters_to_remove, '', line) + ' '
        line = re.sub(self.phrase_to_remove, '', line)
        line = re.sub(self.quotes_on_the_outside_of_words, ' ', line)

        for index in range(len(line)):
            self.processing_string += line[index]

        self.process_current_string()

    def process_line(self, line):
        line = re.sub(self.characters_to_remove, '', line) + ' '
        line = re.sub(self.phrase_to_remove, '', line)
        line = re.sub(self.quotes_on_the_outside_of_words, ' ', line)

        for index in range(len(line)):
            self.processing_string += line[index]
            if line[index] in self.terminators and not line[:index].endswith(
                self.words_that_end_in_periods
            ):
                self.process_current_string()

    def process_current_string(self):
        words = self.processing_string.split()
        # words = (self.length * [""]) + words + (self.length * [""])

        if words:
            self.chain[''].append(words[0])

        for index in range(len(words)):
            key_words = words[max(index - self.length, 0):index]
            for key_index in range(len(key_words)):
                words_combined = " ".join(key_words[key_index:])
                self.chain[words_combined].append(words[index])

        self.processing_string = ""

    def go_go_markov_chain(self):
        # do your thing markov chain
        key_queue = deque()
        key_queue.append('')
        result = []
        output = True
        while output and len(result) < self.maximum_length:
            output = ''
            max_num_of_words_to_try = min(self.length, len(key_queue))
            curr_num_of_words_offset = max_num_of_words_to_try
            while not output and curr_num_of_words_offset:
                key = " ".join(list(key_queue)[
                    max_num_of_words_to_try - curr_num_of_words_offset:]
                )
                value = self.chain[key]
                if value:
                    output = random.choice(value)
                curr_num_of_words_offset -= 1
            result.append(output)
            if len(key_queue) >= self.length:
                key_queue.popleft()
            key_queue.append(output)
        return " ".join(result)

    def __str__(self):
        try:
            result = self.go_go_markov_chain()
            try:
                result = result[0].upper() + result[1:]
            except:
                pass
            return result.encode('ascii', 'ignore')
        except:
            err_msg = traceback.format_exc()
            logging.error('Unexpected error: {}'.format(err_msg))
            self.msg_writer.write_error(err_msg)
            pass
