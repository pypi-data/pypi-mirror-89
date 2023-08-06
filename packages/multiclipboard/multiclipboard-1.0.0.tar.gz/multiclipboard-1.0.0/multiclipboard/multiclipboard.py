#! python3

import shelve, pyperclip, sys, os, errno

class Multiclipboard (): 
    """
    Class to saves and loads pices of text to the clipboard, 
    via a database in a DB file
    """

    def __init__ (self, path_db_file): 
        """
        Constructor of class. Set path to the Db file
        """

        self.path_db_file = path_db_file

        self.__verify_path()

        self.db_file = os.path.dirname (__file__)
        self.__mcbShelf = shelve.open(os.path.join(path_db_file, 'clipboard'))


    def __verify_path (self):
        """
        Verify is the path exist in the pc
        """ 

        if not os.path.exists (self.path_db_file): 
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path_db_file)

    def save_text (self, keyword, text=""): 
        """
        Save specific text or text from clipboard to the database, 
        and associate this text with a keyword
        """
        
        if text == "": 
            self.__mcbShelf [str(keyword)] = pyperclip.paste()
            print ('keyword "{}" saved with clipboard text'.format (keyword))
        else: 
            self.__mcbShelf [str(keyword)] = str(text)
            print ('keyword "{}" saved with specific text'.format (keyword))

    def get_text (self, keyword): 
        """
        Return specific text with keyword
        """

        text = self.__mcbShelf[str(keyword)]
        return text

    def copy_text (self, keyword): 
        """
        Copy to clipboard specific text with keyword
        """

        pyperclip.copy(self.__mcbShelf[str(keyword)])
        print ('Text for the keyword "{}" copied'.format (keyword))

    def delete_keyword (self, keyword): 
        """
        Delete specific keywords and the keyword text
        """

        if str(keyword) in self.__mcbShelf: 
            del self.__mcbShelf[str(keyword)]
            print ('keyword "{}" deleted'.format (keyword))
        else: 
            print ("keyword dooesn't exist")

    def delete_all (self): 
        """
        Delete all keywords from the file
        """

        for item in self.__mcbShelf.keys():
            del self.__mcbShelf[item]

        print ('All keywords delated')


    def list_keywords (self): 
        """ 
        Print all keywords from the file
        """

        print ("\nKeywords: \n")
        for keyword in list(self.__mcbShelf.keys()): 
            print (keyword)


