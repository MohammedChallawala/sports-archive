create database sportsarchive;

use sportsarchive;

-- Table creation

CREATE TABLE suppliers (
    Supplier_ID INT PRIMARY KEY,  -- Assuming you have a Supplier_ID
    Supplier_Name VARCHAR(100) UNIQUE NOT NULL,
    Contact_Info VARCHAR(255) NULL
);

CREATE TABLE sports_sportinfo (
    Sport_ID INT PRIMARY KEY,
    Sport_Name VARCHAR(100) UNIQUE NOT NULL,
    Weight INT,
    Age INT,
    Supplier_ID INT,
    FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID)
);

CREATE TABLE equipment (
    Equipment_ID INT PRIMARY KEY,
    Equipment_Name VARCHAR(100) NOT NULL,
    Weight INT,
    Dimensions VARCHAR(50),
    Sport_ID INT,
    Supplier_Name VARCHAR(100),
    FOREIGN KEY (Sport_ID) REFERENCES sports_sportinfo(Sport_ID),
    FOREIGN KEY (Supplier_Name) REFERENCES suppliers(Supplier_Name)
);

CREATE TABLE players (
    Player_ID INT PRIMARY KEY,
    Age INT NOT NULL,
    Gender VARCHAR(10),
    First_Name VARCHAR(50),
    Middle_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Sponsor_Name VARCHAR(100),
    Sport_ID INT,
    FOREIGN KEY (Sport_ID) REFERENCES sports_sportinfo(Sport_ID)
);
CREATE TABLE organizers (
    Organizer_Name VARCHAR(100) PRIMARY KEY,
    Description TEXT,
    Supplier_Name VARCHAR(100),
    Chairman_FN VARCHAR(50),
    Chairman_MN VARCHAR(50),
    Chairman_LN VARCHAR(50),
    FOREIGN KEY (Supplier_Name) REFERENCES suppliers(Supplier_Name)
);
CREATE TABLE organizers_competitions (
    Organizer_Name VARCHAR(100),
    Competition_Name VARCHAR(100),
    PRIMARY KEY (Organizer_Name, Competition_Name),
    FOREIGN KEY (Organizer_Name) REFERENCES organizers(Organizer_Name)
);
CREATE TABLE competitions (
    Competition_Name VARCHAR(100) PRIMARY KEY,
    Location VARCHAR(100),
    Duration VARCHAR(50)
);
CREATE TABLE sponsors (
    Sponsor_Name VARCHAR(100) PRIMARY KEY,
    Sport_ID INT,
    FOREIGN KEY (Sport_ID) REFERENCES sports_sportinfo(Sport_ID)
);
CREATE TABLE sponsors_budget (
    Sponsor_Name VARCHAR(100),
    Budget DECIMAL(10, 2),
    PRIMARY KEY (Sponsor_Name),
    FOREIGN KEY (Sponsor_Name) REFERENCES sponsors(Sponsor_Name)
);
CREATE TABLE sponsors_competition (
    Sponsor_Name VARCHAR(100),
    Competition_Name VARCHAR(100),
    PRIMARY KEY (Sponsor_Name, Competition_Name),
    FOREIGN KEY (Sponsor_Name) REFERENCES sponsors(Sponsor_Name),
    FOREIGN KEY (Competition_Name) REFERENCES competitions(Competition_Name)
);
CREATE TABLE sponsors_player (
    Sponsor_Name VARCHAR(100),
    Player_ID INT,
    PRIMARY KEY (Sponsor_Name, Player_ID),
    FOREIGN KEY (Sponsor_Name) REFERENCES sponsors(Sponsor_Name),
    FOREIGN KEY (Player_ID) REFERENCES players(Player_ID)
);
CREATE TABLE broadcasters (
    Broadcaster_Name VARCHAR(100) PRIMARY KEY,
    Location VARCHAR(100),
    Competition_Name VARCHAR(100),
    Platform VARCHAR(50),
    Languages VARCHAR(100),
    FOREIGN KEY (Competition_Name) REFERENCES competitions(Competition_Name)
);
CREATE TABLE records (
    Player_ID INT,
    Sport_ID INT,
    Competition_Name VARCHAR(100),
    Tally INT,
    Duration VARCHAR(50),
    PRIMARY KEY (Player_ID, Sport_ID, Competition_Name),
    FOREIGN KEY (Player_ID) REFERENCES players(Player_ID),
    FOREIGN KEY (Sport_ID) REFERENCES sports_sportinfo(Sport_ID),
    FOREIGN KEY (Competition_Name) REFERENCES competitions(Competition_Name)
);
CREATE TABLE sports_sportdetails (
    Sport_Name VARCHAR(100) PRIMARY KEY,
    Number_of_Players INT
);

-- Data population

INSERT INTO suppliers (Supplier_ID, Supplier_Name, Contact_Info) VALUES
(1, 'Athletics Supplier Co.', 'contact@athleticssupplier.com'),
(2, 'Track Masters Inc.', 'info@trackmasters.com'),
(3, 'Football Gear Ltd.', 'sales@footballgear.com'),
(4, 'Basketball Pro Supplies', 'support@basketballpros.com'),
(5, 'Tennis World', 'contact@tennisworld.com'),
(6, 'Hockey Equipment Co.', 'info@hockeyequipment.com'),
(7, 'Cricket Equipment Ltd.', 'sales@cricketequipment.com'),
(8, 'Ping Pong Supplies', 'support@pingpongsupplies.com'),
(9, 'Boxing Gear Pro', 'info@boxinggearpro.com'),
(10, 'Archery Supplies Inc.', 'sales@archerysupplies.com');

INSERT INTO sports_sportinfo (Sport_ID, Sport_Name, Weight, Age, Supplier_ID) VALUES
(1, 'Javelin Throw', 800, 18, 1),
(2, 'Shot Put', 7200, 18, 2),
(3, 'Football', 450, 16, 3),
(4, 'Basketball', 600, 16, 4),
(5, 'Tennis', 300, 16, 5),
(6, 'Hockey', 800, 16, 6),
(7, 'Cricket', 1200, 16, 7),
(8, 'Table Tennis', 150, 12, 8),
(9, 'Boxing', 250, 18, 9),
(10, 'Archery', 1500, 18, 10);

INSERT INTO sports_sportdetails (Sport_Name, Number_of_Players) VALUES
('Javelin Throw', 1),
('Shot Put', 1),
('Football', 22),
('Basketball', 10),
('Tennis', 2),
('Hockey', 6),
('Cricket', 11),
('Table Tennis', 2),
('Boxing', 2),
('Archery', 1);

INSERT INTO equipment (Equipment_ID, Equipment_Name, Weight, Dimensions, Sport_ID, Supplier_Name) VALUES
(1, 'Javelin', 800, '2.6m', 1, 'Athletics Supplier Co.'),
(2, 'Shot Put', 7200, '12cm', 2, 'Track Masters Inc.'),
(3, 'Football', 450, '22cm', 3, 'Football Gear Ltd.'),
(4, 'Basketball', 600, '24cm', 4, 'Basketball Pro Supplies'),
(5, 'Tennis Racket', 300, '68cm', 5, 'Tennis World'),
(6, 'Hockey Stick', 800, '95cm', 6, 'Hockey Equipment Co.'),
(7, 'Cricket Bat', 1200, '85cm', 7, 'Cricket Equipment Ltd.'),
(8, 'Table Tennis Paddle', 150, '17cm', 8, 'Ping Pong Supplies'),
(9, 'Boxing Gloves', 250, '30cm', 9, 'Boxing Gear Pro'),
(10, 'Archery Bow', 1500, '1.5m', 10, 'Archery Supplies Inc.');

INSERT INTO competitions (Competition_Name, Location, Duration) VALUES 
('Summer Olympics 2020', 'Tokyo', '30 Days'),
('Winter Olympics 2018', 'Pyeongchang', '17 Days'),
('Asian Games 2018', 'Jakarta', '15 Days'),
('Tour de France 2021', 'France', '23 Days'),
('ICC Cricket World Cup 2019', 'England', '50 Days'),
('Australian Open 2020', 'Melbourne', '14 Days'),
('UEFA Champions League 2019', 'Europe', '275 Days'),
('Super Bowl 2020', 'Miami', '1 Day'),
('NBA Finals 2021', 'USA', '7 Days'),
('Stanley Cup 2021', 'Canada', '60 Days');

INSERT INTO sponsors (Sponsor_Name, Sport_ID) VALUES 
('Nike', 1),
('Adidas', 2),
('Puma', 3),
('Under Armour', 4),
('Reebok', 5);

INSERT INTO sponsors_budget (Sponsor_Name, Budget) VALUES 
('Nike', 1000000.00),
('Adidas', 500000.00),
('Puma', 300000.00),
('Under Armour', 200000.00),
('Reebok', 150000.00);

INSERT INTO players (Player_ID, Age, Gender, First_Name, Middle_Name, Last_Name, Sponsor_Name, Sport_ID) VALUES 
(1, 24, 'Male', 'Usain', 'Bolt', 'Bolt', 'Nike', 1),
(2, 29, 'Female', 'Serena', NULL, 'Williams', 'Adidas', 5),
(3, 27, 'Male', 'Lionel', NULL, 'Messi', 'Puma', 3),
(4, 26, 'Female', 'Simone', NULL, 'Biles', 'Under Armour', 2),
(5, 32, 'Male', 'LeBron', NULL, 'James', 'Nike', 4);

INSERT INTO organizers (Organizer_Name, Description, Supplier_Name, Chairman_FN, Chairman_MN, Chairman_LN) VALUES  
('Olympics Committee', 'Responsible for organizing the Summer and Winter Olympic Games.', 'Athletics Supplier Co.', 'Thomas', 'A.', 'Bach'), 
('FIFA', 'Governing body of football (soccer) worldwide.', 'Football Gear Ltd.', 'Gianni', NULL, 'Infantino'), 
('UEFA', 'Governing body for European football.', 'Football Gear Ltd.', 'Aleksander', NULL, 'Ceferin'), 
('NCAA', 'Organizes college athletics and educational programs.', 'Track Masters Inc.', 'Mark', 'L.', 'Emmert'), 
('International Cricket Council', 'Governing body for international cricket.', 'Cricket Equipment Ltd.', 'Shahid', 'A.', 'Afridi');

INSERT INTO organizers_competitions (Organizer_Name, Competition_Name) VALUES 
('Olympics Committee', 'Summer Olympics 2020'),
('FIFA', 'World Cup 2018'),
('UEFA', 'UEFA Champions League 2019'),
('NCAA', 'NCAA Championships'),
('International Cricket Council', 'ICC Cricket World Cup 2019');

INSERT INTO sponsors_competition (Sponsor_Name, Competition_Name) VALUES  
('Nike', 'Summer Olympics 2020'), 
('Adidas', 'Winter Olympics 2018'), 
('Puma', 'ICC Cricket World Cup 2019'), 
('Under Armour', 'Asian Games 2018'), 
('Reebok', 'Australian Open 2020');


INSERT INTO sponsors_player (Sponsor_Name, Player_ID) VALUES 
('Nike', 1),
('Adidas', 2),
('Puma', 3),
('Under Armour', 4),
('Nike', 5);

INSERT INTO broadcasters (Broadcaster_Name, Location, Competition_Name, Platform, Languages) VALUES 
('ESPN', 'USA', 'Summer Olympics 2020', 'Cable', 'English, Spanish'),
('NBC Sports', 'USA', 'Winter Olympics 2018', 'Cable', 'English'),
('Sky Sports', 'UK', 'UEFA Champions League 2019', 'Cable', 'English'),
('Fox Sports', 'USA', 'Stanley Cup 2021', 'Cable', 'English'),
('BeIN Sports', 'Middle East', 'ICC Cricket World Cup 2019', 'Satellite', 'Arabic, English');

INSERT INTO records (Player_ID, Sport_ID, Competition_Name, Tally, Duration) VALUES 
(1, 1, 'Summer Olympics 2020', 3, '9.58 sec'),
(2, 5, 'Winter Olympics 2018', 7, '1 hr 30 min'),
(3, 3, 'UEFA Champions League 2019', 10, '120 min'),
(4, 2, 'NBA Finals 2021', 5, '10.1 sec'),
(5, 4, 'ICC Cricket World Cup 2019', 2, '4.2 sec');


INSERT INTO broadcasters (Broadcaster_Name, Location, Competition_Name, Platform, Languages) VALUES 
('DAZN', 'Germany', 'Tour de France 2021', 'Streaming', 'German'),
('TSN', 'Canada', 'NBA Finals 2021', 'Cable', 'French'),
('Eurosport', 'France', 'Australian Open 2020', 'Satellite', 'English'),
('Al Jazeera Sports', 'Qatar', 'Asian Games 2018', 'Satellite', 'Arabic'),
('Star Sports', 'India', 'Super Bowl 2020', 'Cable', 'Hindi');

INSERT INTO organizers (Organizer_Name, Description, Supplier_Name, Chairman_FN, Chairman_MN, Chairman_LN) VALUES  
('Asian Games Committee', 'Organizes and promotes the Asian Games for athletes across Asia.', 'Track Masters Inc.', 'Ahmed', 'H.', 'Khan'), 
('International Tennis Federation', 'Governing body for world tennis, setting rules and organizing events.', 'Tennis World', 'David', 'H.', 'Haggerty'), 
('International Basketball Federation', 'Global governing body for basketball events and regulations.', 'Basketball Pro Supplies', 'Hamane', NULL, 'Niang'), 
('World Athletics', 'Governing body for track and field events worldwide.', 'Athletics Supplier Co.', 'Sebastian', 'X.', 'Coe'), 
('World Rugby', 'Responsible for promoting and organizing rugby tournaments globally.', 'Cricket Equipment Ltd.', 'Bill', NULL, 'Beaumont');

INSERT INTO organizers_competitions (Organizer_Name, Competition_Name) VALUES 
('Asian Games Committee', 'Asian Games 2018'),
('International Tennis Federation', 'Australian Open 2020'),
('International Basketball Federation', 'NBA Finals 2021'),
('World Athletics', 'Tour de France 2021'),
('World Rugby', 'Rugby World Cup 2019');

INSERT INTO players (Player_ID, Age, Gender, First_Name, Middle_Name, Last_Name, Sponsor_Name, Sport_ID) VALUES 
(6, 28, 'Male', 'Roger', NULL, 'Federer', 'Wilson', 5),
(7, 30, 'Female', 'Megan', NULL, 'Rapinoe', 'Nike', 3),
(8, 22, 'Male', 'Naomi', NULL, 'Osaka', 'Yonex', 5),
(9, 25, 'Female', 'Katie', NULL, 'Ledecky', 'Speedo', 2),
(10, 31, 'Male', 'Virat', NULL, 'Kohli', 'Puma', 6);

INSERT INTO records (Player_ID, Sport_ID, Competition_Name, Tally, Duration) VALUES 
(6, 5, 'Australian Open 2020', 5, '3 hrs 12 min'),
(7, 3, 'Winter Olympics 2018', 6, '90 min'),
(8, 5, 'Asian Games 2018', 4, '2 hrs 15 min'),
(9, 2, 'Summer Olympics 2020', 4, '15.8 sec'),
(10, 6, 'Tour de France 2021', 1, '85 hrs 37 min');

INSERT INTO sponsors (Sponsor_Name, Sport_ID) VALUES 
('Coca-Cola', 1),
('PepsiCo', 2),
('Red Bull', 3),
('Gatorade', 4),
('Visa', 5);

INSERT INTO sponsors_budget (Sponsor_Name, Budget) VALUES 
('Coca-Cola', 800000.00),
('PepsiCo', 600000.00),
('Red Bull', 350000.00),
('Gatorade', 400000.00),
('Visa', 900000.00);

INSERT INTO sponsors_competition (Sponsor_Name, Competition_Name) VALUES  
('Coca-Cola', 'Summer Olympics 2020'), 
('PepsiCo', 'Super Bowl 2020'), 
('Red Bull', 'Tour de France 2021'), 
('Gatorade', 'Winter Olympics 2018'), 
('Visa', 'UEFA Champions League 2019');

INSERT INTO sponsors_player (Sponsor_Name, Player_ID) VALUES 
('Coca-Cola', 6),
('PepsiCo', 7),
('Red Bull', 8),
('Gatorade', 9),
('Visa', 10);

use sportsarchive;
CREATE TABLE users (
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);
INSERT INTO users (username, password, role) VALUES ('admin', 'adminpassword', 'admin');
