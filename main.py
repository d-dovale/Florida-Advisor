import sys
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow,
    QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter, QDialog,
    QTableView, QHeaderView, QTableWidget
)
import webbrowser
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QPixmap, QMovie, QStandardItemModel, QStandardItem, QFont, QFontDatabase
import sqlite3

choice = "Location"
location = "Type"
price = "Price"
time = "Time"
amenities = "Internet"

choiceIndex = 0
locationIndex = 0
priceIndex = 0
timeIndex = 0
amenitiesIndex = 0

# List of attractions and their attributes
    #name: [type[0], location[1], price[2], time[3], amenities[4]]

widget_names = {
    "Adventure Landing": ['Family', 'North Florida', '$', 'All Day', 'Wifi'],
    "Bern's Steak House": ['Food', 'Central Florida', '$$$', 'Night', 'Wifi'],
    "Bioluminescent Kayak Tours": ['Nature', 'Central Florida', '$$', 'Night', 'No Wifi'],
    "Blue Heaven": ['Food', 'South Florida', '$$', 'Day', 'No Wifi'],
    "Bok Tower And Gardens": ['Nature', 'Central Florida', '$$', 'Day', 'Wifi'],
    "Bonnet House Museum & Gardens": ['Nature', 'South Florida', '$', 'Day', 'Wifi'],
    "Clearwater Beach": ['Nature', 'Central Florida', 'Free', 'All Day', 'No Wifi'],
    "Clyde Butcher’s Gallery": ['Art', 'South Florida', 'Free', 'Day', 'No Wifi'],
    "Cummer Museum of Art & Gardens": ['Art', 'North Florida', '$', 'Day', 'No Wifi'],
    "Dali Museum": ['Art', 'Central Florida', '$', 'Day', 'Wifi'],
    "Disney Springs": ['Family', 'Central Florida', 'Free', 'All Day', 'Wifi'],
    "Disney World": ['Family', 'Central Florida', '$$$', 'Day', 'Wifi'],
    "Dry Tortugas National Park": ['Nature', 'South Florida', '$', 'All Day', 'No Wifi'],
    "Epcot": ['Family', 'Central Florida', '$$$', 'Day', 'Wifi'],
    "Ernest Hemingway Home And Museum": ['History and Culture', 'South Florida', '$', 'Day', 'No Wifi'],
    "Everglades National Park": ['Nature', 'South Florida', '$', 'All Day', 'No Wifi'],
    "Flora-Bama Lounge": ['Food', 'North Florida', '$$', 'Day', 'No Wifi'],
    "Florida Caverns State Park": ['Nature', 'North Florida', '$', 'Day', 'No Wifi'],
    "Ghosts and Gravestones Trolley Tour": ['Family', 'South Florida', '$', 'Night', 'No Wifi'],
    "Hollywood Beach Boardwalk": ['Nature', 'South Florida', 'Free', 'All Day', 'No Wifi'],
    "Joe’s Stone Crab": ['Food', 'South Florida', '$$', 'Day', 'No Wifi'],
    "John Pennekamp Coral Reef State Park": ['Nature', 'South Florida', '$', 'Day', 'Wifi'],
    "Kennedy Space Center": ['History and Culture', 'Central Florida', '$$', 'Day', 'Wifi'],
    "Legoland": ['Family', 'Central Florida', '$$$', 'Day', 'Wifi'],
    "Lowry Park Zoo": ['Nature', 'Central FLorida', 'Free', 'All Day', 'No Wifi'],
    "MOTE Marine Laboratory": ['Nature', 'South Florida', '$', 'Day', 'Wifi'],
    "McGuire's Irish Pub": ['Food', 'North Florida', '$$', 'Day', 'No Wifi'],
    "Miami South Beach": ['Nature', 'South Florida', 'Free', 'All Day', 'No Wifi'],
    "Miccosukee Reservation": ['History and Culture', 'South Florida', '$', 'Day', 'No Wifi'],
    "Moonlight Zipline Safari": ['Nature', 'Central Florida', '$$', 'Night', 'No Wifi'],
    "Murder Mystery Dinner Train": ['Family', 'South Florida', '$$$', 'Day', 'No Wifi'],
    "Myakka State Park": ['Nature', 'South Florida', '$', 'Day', 'Wifi'],
    "Naples Botanical Garden": ['Nature', 'South Florida', '$', 'Day', 'No Wifi'],
    "Ocala National Forest": ['Nature', 'Central Florida', 'Free', 'All Day', 'No Wifi'],
    "Private Moon-Watch Boat Cruise": ['Family', 'South Florida', '$', 'Day', 'Wifi'],
    "Pérez Art Museum Miami": ['Art', 'North Florida', '$', 'Day', 'No Wifi'],
    "Ringling Museum And Ca D'Zan Mansion": ['History and Culture', 'South Florida', '$', 'Day', 'No Wifi'],
    "Satchel's Pizza": ['Food', 'North Florida', '$$', 'All Day', 'Wifi'],
    "SeaWorld Orlando": ['Family', 'Central Florida', '$$$', 'Day', 'Wifi'],
    "Seacrest Wolf Preserve": ['Nature', 'North Florida', '$', 'Day', 'Wifi'],
    "St. Andrews State Park": ['Nature', 'South Florida', '$', 'Day', 'Wifi'],
    "St. Augustine Distillery": ['Food', 'North Florida', 'Free', 'Day', 'No Wifi'],
    "Sunken Gardens": ['Nature', 'Central Florida', '$', 'Day', 'Wifi'],
    "The John and Mable Ringling Museum of Art": ['Art', 'South Florida', '$', 'Day', 'No Wifi'],
    "The Le Tub Saloon": ['Food', 'South Florida', '$$', 'Day', 'No Wifi'],
    "Universal Studios": ['Family', 'Central Florida', '$$$', 'Day', 'Wifi'],
    "Venetian Pool": ['History and Culture', 'South Florida', '$', 'Day', 'No Wifi'],
    "Vero Beach Museum of Art": ['Art', 'South Florida', '$', 'Day', 'No Wifi'],
    "Vizcaya Museum And Gardens": ['History and Culture', 'South Florida', '$', 'Day', 'No Wifi'],
    "Withlacoochee State Trail": ['Nature', 'Central Florida', 'Free', 'Day', 'No Wifi'],
    "Wynwood Walls": ['Art', 'South Florida', 'Free', 'Day', 'No Wifi']

    }

# Initial title screen
class TitleScreen(QDialog):
    def __init__(self):
        super(TitleScreen, self).__init__()
        loadUi("TitleScreen.ui",self)
        
        # Starts the animation for the gif
        self.movie = QMovie("Images/title.gif")
        self.title.setMovie(self.movie)
        self.movie.start()

        # Fonts
        QFontDatabase.addApplicationFont("fonts/Nexa Bold.otf")
        QFontDatabase.addApplicationFont("fonts/Nexa Light.otf")

        # Links the backButton to the function goback
        self.startButton.clicked.connect(self.gotomain)
        self.helpButton.clicked.connect(self.gotohelp)

    def gotomain(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohelp(self):
        help = HelpScreen()
        widget.addWidget(help)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    
# Screen where user chooses options
class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("MainScreen.ui",self)
        
        # Starts the animation for the gif
        self.movie = QMovie("Images/attration generator.gif")
        self.title.setMovie(self.movie)
        self.movie.start()

        # Links the backButton to the function goback
        self.searchButton.clicked.connect(self.pressed)
        self.backButton.clicked.connect(self.goback)

        # Saves the choice that the user selected if the user goes back to the MainScreen
        self.typeChoice.setCurrentIndex(choiceIndex)
        self.typeLocation.setCurrentIndex(locationIndex)
        self.typePrice.setCurrentIndex(priceIndex)
        self.typeTime.setCurrentIndex(timeIndex)
        self.typeAmenities.setCurrentIndex(amenitiesIndex)

    def gotolist(self):
        lst = ListScreen()
        widget.addWidget(lst)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # Submits choices and changes to ListScreen
    def pressed(self):
        global choice
        global location
        global price
        global time 
        global amenities

        global choiceIndex
        global locationIndex
        global priceIndex
        global timeIndex
        global amenitiesIndex

        choice = self.typeChoice.currentText()
        location = self.typeLocation.currentText()
        price = self.typePrice.currentText()
        time = self.typeTime.currentText()
        amenities = self.typeAmenities.currentText()

        choiceIndex = self.typeChoice.currentIndex()
        locationIndex = self.typeLocation.currentIndex()
        priceIndex = self.typePrice.currentIndex()
        timeIndex = self.typeTime.currentIndex()
        amenitiesIndex = self.typeAmenities.currentIndex()

        self.gotolist()

    def goback(self):
        title = TitleScreen()
        widget.addWidget(title)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Help Screen
class HelpScreen(QDialog):
    def __init__(self):
        super(HelpScreen, self).__init__()
        loadUi("HelpScreen.ui",self)
        
        # Starts the animation for the gif
        self.movie = QMovie("Images/Help Center.gif")
        self.title.setMovie(self.movie)
        self.movie.start()

        # Links the backButton to the function goback
        self.backButton.clicked.connect(self.goback)

    def goback(self):
        title = TitleScreen()
        widget.addWidget(title)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# Screen displaying list of sorted attractions
class ListScreen(QDialog, QWidget):
    def __init__(self):
        super(ListScreen, self).__init__()
        _translate = QtCore.QCoreApplication.translate
        self.setStyleSheet("background:rgb(45, 113, 156)")
        mainLayout = QVBoxLayout()   # Controls container layout.
        
        labelsDisplayed = 0
        for name, attributes in widget_names.items():
            if(((choice == attributes[0]) or (choice == "Type")) and ((location == attributes[1]) or (location == "Location")) and ((price == attributes[2]) or (price == "Price")) and ((time == attributes[3]) or (time == "Time")) and ((amenities == attributes[4]) or (amenities == "Internet"))): 
                labelsDisplayed+=1


        model = QStandardItemModel(labelsDisplayed,1)
        model.setHorizontalHeaderLabels(["Attractions"])


        # Goes through all the selections and sorts them based off of what they chose 
        count = 0
        for name, attributes in widget_names.items():
            if(((choice == attributes[0]) or (choice == "Type")) and ((location == attributes[1]) or (location == "Location")) and ((price == attributes[2]) or (price == "Price")) and ((time == attributes[3]) or (time == "Time")) and ((amenities == attributes[4]) or (amenities == "Internet"))):
                item = QStandardItem(name)
                model.setItem(count, 0, item)
                count+=1
                
                if count%2 == 0:
                    item.setBackground(QtGui.QColor(250,250,250))
                        



        # Search filter
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        # Search Bar
        search_field = QLineEdit()
        search_field.setStyleSheet('background:rgb(221, 255, 252); font-size: 30px; height: 35px;')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)


        # Table
        table = QTableView()
        
        table.setStyleSheet('font-size: 35px; background:rgb(255,255,255)')
        table.horizontalHeader().setStyleSheet("::section{Background-color:rgb(254, 255, 227);}")
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.verticalHeader().setDefaultSectionSize(90);
        table.horizontalHeader().setHighlightSections(False)

        table.setModel(filter_proxy_model)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)


        # Adding Completer.
        #completer = QCompleter(widget_names)
        #completer.setCaseSensitivity(Qt.CaseInsensitive)
        #search_field.setCompleter(completer)

        
        #Back Button
        font = QtGui.QFont()
        font.setFamily("Nexa Light")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        backButton = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(25)
        backButton.setFont(font)
        backButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(99, 99, 99);\n"
"    border: none;\n"
"    padding-top: 5px;\n"
"    color: rgb(226, 234, 216);\n"
"    border-radius: 20px;\n"
"    border-left: 1px solid rgb(110, 114, 76);\n"
"    border-right: 2px solid rgb(110, 114, 76);\n"
"    border-bottom: 3px solid rgb(110, 114, 76);\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(134, 134, 134);\n"
"    border-left: 1px solid rgb(110, 114, 76);\n"
"    border-right: 1px solid rgb(110, 114, 76);\n"
"    border-radius: 20px;\n"
"    border-bottom: 4px solid rgb(110, 114, 76);\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-left: 1px solid rgb(110, 114, 76);\n"
"    border-right: 1px solid rgb(110, 114, 76);\n"
"    border-top: 0px solid rgb(110, 114, 76);\n"
"    border-radius: 20px;\n"
"    padding-top: -5x;\n"
"    border-bottom: none;\n"
"\n"
"}")

        backButton.setGeometry(QtCore.QRect(259, 210, 5, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(backButton.sizePolicy().hasHeightForWidth())
        backButton.setSizePolicy(sizePolicy)
        backButton.setText(_translate("HelpScreen", " ← "))


        mainLayout.addWidget(search_field)
        mainLayout.addWidget(table)
        mainLayout.addWidget(backButton)

        backButton.clicked.connect(self.goback)
        table.clicked.connect(self.getLink)
        self.setLayout(mainLayout)

    def goback(self):
        main = MainScreen()
        widget.addWidget(main)
        widget.setCurrentIndex(widget.currentIndex() + 1)



    def getLink(self, table):
        row = table.row()
        row_name = table.data(0)
            
        index = list(widget_names.keys()).index(row_name)
                         

        if index == 0:
            Adventure_Landing = webbrowser.open("www.adventurelanding.com")
        if index == 1:
            Berns_Steak_House = webbrowser.open("https://bernssteakhouse.com/%27")
        if index == 2:
            Bioluminescent_Kayak_Tours = webbrowser.open("https://bioluminescencetours.com/?gclid=Cj0KCQiA47GNBhDrARIsAKfZ2rCVuRVeCgqcI9OZoCrdr8RH-BkYYxQZxIdSMd3N4mWquNvT3qFbqxEaArGHEALw_wcB")
        if index == 3:
            Blue_Heaven = webbrowser.open("https://blueheavenkw.com/")
        if index == 4:
            Bok_Tower_And_Gardens = webbrowser.open("https://boktowergardens.org/")
        if index == 5:
            Bonnet_House_Museum_Gardens = webbrowser.open("https://www.bonnethouse.org/")
        if index == 6:
            Clearwater_Beach = webbrowser.open("https://www.visitstpeteclearwater.com/communities/clearwater-beach")
        if index == 7:
            Clyde_Butchers_Gallery = webbrowser.open("https://clydebutcher.com/galleries/")
        if index == 8:
            Cummer_Museum_of_Art_Gardens = webbrowser.open("https://www.cummermuseum.org/")
        if index == 9:
            Dali_Museum = webbrowser.open("https://thedali.org/")
        if index == 10:
            Disney_Springs = webbrowser.open("https://www.disneysprings.com/")
        if index == 11:
            Disney_World = webbrowser.open("https://disneyworld.disney.go.com/")
        if index == 12:
            Dry_Tortugas_National_Park = webbrowser.open("https://www.nps.gov/drto/index.htm")
        if index == 13:
            Epcot = webbrowser.open("https://disneyworld.disney.go.com/destinations/epcot/")
        if index == 14:
            Ernest_Hemingway_Home_And_Museum = webbrowser.open("https://www.hemingwayhome.com/")
        if index == 15:
            Everglades_National_Park = webbrowser.open("https://www.nps.gov/ever/index.htm")
        if index == 16:
            FloraBama_Lounge = webbrowser.open("http://www.florabama.com/")
        if index == 17:
            Florida_Caverns_State_Park = webbrowser.open("https://www.floridastateparks.org/parks-and-trails/florida-caverns-state-park")
        if index == 18:
            Ghosts_Gravestones_Trolley_Tour = webbrowser.open("https://www.ghostsandgravestones.com/")
        if index == 19:
            Hollywood_Beach_Boardwalk = webbrowser.open("https://www.floridashollywood.org/hollywood-beach-broadwalk/")
        if index == 20:
            Joe_Stone_Crab = webbrowser.open("https://www.joesstonecrab.com/")
        if index == 21:
            John_Pennekamp_Coral_Reef_State_Park = webbrowser.open("https://www.pennekamppark.com/")
        if index == 22:
            Kennedy_Space_Center = webbrowser.open("https://www.kennedyspacecenter.com/")
        if index == 23:
            Legoland = webbrowser.open("https://www.legoland.com/florida/")
        if index == 24:
            Lowry_Park_Zoo = webbrowser.open("https://zootampa.org/")
        if index == 25:
            MOTE_Marine_Laboratory = webbrowser.open("https://mote.org/")
        if index == 26:
            McGuires_Irish_Pug = webbrowser.open("https://www.mcguiresirishpub.com/")
        if index == 27:
            Miami_South_Beach = webbrowser.open("https://www.visitflorida.com/places-to-go/southeast/south-beach/")
        if index == 28:
            Miccosukee_Reservation = webbrowser.open("https://www.miccosukee.com/history")
        if index == 29:
            Moonlight_Zipline_Safari = webbrowser.open("https://www.zipontampabay.com/moonlight-canopy-tours/")
        if index == 30:
            Murder_Mystery_Dinner_Train = webbrowser.open("https://semgulf.com/")
        if index == 31:
            Myakka_State_Park = webbrowser.open("https://www.floridastateparks.org/parks-and-trails/myakka-river-state-park")
        if index == 32:
            Naples_Botanical_Garden = webbrowser.open("https://www.naplesgarden.org/")
        if index == 33:
            Ocala_National_Forest = webbrowser.open("https://stateparks.com/ocala_national_forest_in_florida.html")
        if index == 34:
            Private_MoonWatch_Boat_Cruise = webbrowser.open("https://www.viator.com/tours/Miami/Private-moon-watch-party-with-Prosecco-on-Boat/d662-284808P5")
        if index == 35:
            Pérez_Art_Museum_Miami = webbrowser.open("https://www.pamm.org/")
        if index == 36:
            Ringling_Museum_And_CaDZan_Mansion = webbrowser.open("https://www.ringling.org/ca-dzan")
        if index == 37:
            Satchels_Pizza = webbrowser.open("https://www.satchelspizza.com/")
        if index == 38:
            SeaWorld_Orlando = webbrowser.open("https://seaworld.com/orlando/")
        if index == 39:
            Seacrest_Wolf_Preserve = webbrowser.open("https://www.seacrestwolfpreserve.org/")
        if index == 40:
            St_Andrews_State_Park = webbrowser.open("https://www.floridastateparks.org/parks-and-trails/st-andrews-state-park")
        if index == 41:
            St_Augustine_Distillery = webbrowser.open("https://www.staugustinedistillery.com/")
        if index == 42:
            Sunken_Gardens = webbrowser.open("https://www.stpete.org/visitors/sunken_gardens.php")
        if index == 43:
            The_John_and_Mable_Ringling_Museum_of_Art = webbrowser.open("https://www.ringling.org/")
        if index == 44:
            The_Le_Tub_Saloon = webbrowser.open("https://www.theletub.com/")
        if index == 45:
            Universal_Studios = webbrowser.open("https://www.universalorlando.com/web/en/us")
        if index == 46:
            Venetian_Pool = webbrowser.open("https://www.coralgables.com/venetianpool")
        if index == 47:
            Vero_Beach_Museum_of_Art = webbrowser.open("https://www.vbmuseum.org/")
        if index == 48:
            Vizcaya_Museum_And_Gardens = webbrowser.open("https://vizcaya.org/")
        if index == 49:
            Withlacoochee_State_Trail = webbrowser.open("https://www.floridastateparks.org/parks-and-trails/withlacoochee-state-trail")
        if index == 50:
            Wynwood_Wall = webbrowser.open("https://thewynwoodwalls.com/")


# main
app = QApplication(sys.argv)
title = TitleScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(title)
widget.setFixedHeight(600)
widget.setFixedWidth(950)
widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")