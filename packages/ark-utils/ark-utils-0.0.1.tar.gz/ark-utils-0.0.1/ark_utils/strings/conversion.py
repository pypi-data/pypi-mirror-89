"""
# Copyright 2020 Xiang Wang, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at 
# http://www.apache.org/licenses/LICENSE-2.0

Author: Xiang Wang, xiangking1995@163.com
Status: Active
"""


def angle_full2half(source_string:str):
    """
    Character string full angle half angle

    :param source_string: (string) string to be processed
    """
    rstring = ""
    for uchar in source_string:
        inside_code=ord(uchar)
        if inside_code == 12288:          
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): 
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring
