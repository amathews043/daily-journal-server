CREATE TABLE Moods (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

INSERT INTO Moods VALUES (null, 'Happy');


INSERT INTO Moods VALUES (null, "Sad");
INSERT INTO Moods VALUES (null, "Angry"); 
INSERT INTO Moods VALUES (null, "Ok"); 


SELECT * FROM Entries


CREATE TABLE Entries (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL, 
    `date` TIMESTAMP NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);


INSERT INTO Entries VALUES (null, "JavaScript", 
"I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.",
1, "Wed Sep 15 2021 10:10:47 ")


INSERT INTO Entries VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 
3, "Wed Sep 15 2021 10:13:11 "); 
INSERT INTO Entries VALUES (null, "JavaScript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.",
3, "Wed Sep 15 2021 10:14:05 "); 

DROP TABLE Entries