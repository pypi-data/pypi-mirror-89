from .dir_entry import DirEntry


class D81DirEntry(DirEntry):
    FTYPE_STR = ('DEL', 'SEQ', 'PRG', 'USR', 'REL', 'CBM', '???', '???')
