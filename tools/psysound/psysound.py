import galaxy.datatypes.data as data
import galaxy.datatypes.binary
from galaxy.datatypes.binary import Binary

class Matlab(Binary):

    file_ext = "mat"
    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )
 
    def sniff( self, filename ):
        # The header of any psysound matlab file starts with "MATLAB 5.0 MAT-file", and the file is binary. 
    # (see: https://maxwell.ict.griffith.edu.au/spl/matlab-page/matfile_format.pdf)
        try:
            header = open( filename ).read()
            if "MATLAB" in header and "5.0" in header:
                return True
            else: 
                return False
        except:
            return False

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek  = "Matlab Binary file"
            dataset.blurb = data.nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'
    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Matlab Binary file (%s)" % ( data.nice_size( dataset.get_size() ) )

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, size=None, offset=None, **kwd):
        if preview:    
            return ("MATLAB data files cannot be previewed.")
        else:
            return super(Matlab, self).display_data( trans, dataset, preview, filename, to_ext, size, offset, **kwd)
    
Binary.register_sniffable_binary_format("mat", "mat", Matlab)

class Wav(Binary):

    file_ext = "wav"
    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )
 
    def sniff( self, filename ):
        try:
            header = open( filename ).read()
            if header.starts_with("RIFF"):
                return True
            else: 
                return False
        except:
            return False

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek  = "Audio (WAV) file"
            dataset.blurb = data.nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'
    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Audio (WAV) file (%s)" % ( data.nice_size( dataset.get_size() ) )

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, size=None, offset=None, **kwd):
        if preview:    
            return ("WAV audio files cannot be previewed.")
        else:
            return super(Wav, self).display_data( trans, dataset, preview, filename, to_ext, size, offset, **kwd)      

Binary.register_unsniffable_binary_ext("wav")
    
class Mp3(Binary):

    file_ext = "mp3"
    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek  = "Audio (MP3) file"
            dataset.blurb = data.nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'
    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Audio (MP3) file (%s)" % ( data.nice_size( dataset.get_size() ) )

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, size=None, offset=None, **kwd):
        if preview:    
            return ("MP3 audio files cannot be previewed.")
        else:
            return super(Mp3, self).display_data( trans, dataset, preview, filename, to_ext, size, offset, **kwd)      

Binary.register_unsniffable_binary_ext("mp3")
    
class Avi(Binary):

    file_ext = "avi"
    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek  = "Video (AVI) file"
            dataset.blurb = data.nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'
    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Video (AVI) file (%s)" % ( data.nice_size( dataset.get_size() ) )

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, size=None, offset=None, **kwd):
        if preview:    
            return ("AVI video files cannot be previewed.")
        else:
            return super(Avi, self).display_data( trans, dataset, preview, filename, to_ext, size, offset, **kwd)      

Binary.register_unsniffable_binary_ext("avi")

class Ogg(Binary):

    file_ext = "ogg"
    def __init__( self, **kwd ):
        Binary.__init__( self, **kwd )

    def set_peek( self, dataset, is_multi_byte=False ):
        if not dataset.dataset.purged:
            dataset.peek  = "Media (OGG) file"
            dataset.blurb = data.nice_size( dataset.get_size() )
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'
    def display_peek( self, dataset ):
        try:
            return dataset.peek
        except:
            return "Media (OGG) file (%s)" % ( data.nice_size( dataset.get_size() ) )

    def display_data(self, trans, dataset, preview=False, filename=None, to_ext=None, size=None, offset=None, **kwd):
        if preview:    
            return ("OGG media files cannot be previewed.")
        else:
            return super(Ogg, self).display_data( trans, dataset, preview, filename, to_ext, size, offset, **kwd)

Binary.register_unsniffable_binary_ext("ogg")