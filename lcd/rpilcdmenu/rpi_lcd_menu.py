from rpilcdmenu.base_menu import BaseMenu
#from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd
from lcd_drive.lcd_uart import LCDUart

class RpiLCDMenu(BaseMenu):
    def __init__(self):
        """
        Initialize menu
        """

        self.lcd = LCDUart()

        self.lcd.lcd_config()
        self.clearDisplay()

        super(self.__class__, self).__init__()

    def clearDisplay(self):
        """
        Clear LCD Screen
        """
        self.lcd.lcd_clear()
        
        return self

    def message(self, text):
        """ Send long string to LCD. 17th char wraps to second line"""
        for char in text:
            self.lcd.lcd_write(char)

        return self

    def displayTestScreen(self):
        """
        Display test screen to see if your LCD screen is wokring
        """
        self.message('Hum. body 36,6\nThis is test')

        return self

    def render(self):
        """
        Render menu
        """
        self.clearDisplay()

        if len(self.items) == 0:
            self.message('Menu is empty')
            return self
        elif len(self.items) <= 2:
            options = (self.current_option == 0 and ">" or " ") + self.items[0].text
            if len(self.items) == 2:
                options += "\n" + (self.current_option == 1 and ">" or " ") + self.items[1].text
            print(options)
            self.message(options)
            return self

        options = ">" + self.items[self.current_option].text

        if self.current_option + 1 < len(self.items):
            options += "\n " + self.items[self.current_option + 1].text
        else:
            options += "\n " + self.items[0].text

        self.message(options)

        return self
