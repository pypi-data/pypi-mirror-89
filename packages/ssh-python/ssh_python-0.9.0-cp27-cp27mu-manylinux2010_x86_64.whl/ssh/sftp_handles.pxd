# This file is part of ssh-python.
# Copyright (C) 2018 Panos Kittenis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, version 2.1.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-130

from sftp cimport SFTP
from sftp_attributes cimport SFTPAttributes

cimport c_sftp


cdef class SFTPFile:
    cdef c_sftp.sftp_file _file
    cdef readonly SFTP sftp
    cdef readonly bint closed

    @staticmethod
    cdef SFTPFile from_ptr(c_sftp.sftp_file _file, SFTP sftp)


cdef class SFTPDir:
    cdef c_sftp.sftp_dir _dir
    cdef readonly SFTP sftp
    cdef readonly bint closed

    @staticmethod
    cdef SFTPDir from_ptr(c_sftp.sftp_dir _dir, SFTP sftp)

    cpdef SFTPAttributes readdir(self)
