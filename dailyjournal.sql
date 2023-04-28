CREATE TABLE Moods (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

INSERT INTO Moods VALUES (null, 'Happy');


INSERT INTO Moods VALUES (null, "Sad");
INSERT INTO Moods VALUES (null, "Angry"); 
INSERT INTO Moods VALUES (null, "Ok"); 


SELECT * FROM Moods


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

CREATE TABLE Tags (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `name` TEXT NOT NULL
)

CREATE TABLE Entry_Tags (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    `entry_id` INTEGER NOT NULL, 
    `tag_id` INTEGER NOT NULL, 
    FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
)

INSERT INTO Tags VALUES (null, "JavaScript");
INSERT INTO Tags VALUES (null, "Python");
INSERT INTO Tags Values (null, "React");
INSERT INTO Tags VALUES (null, "Django");

SELECT * FROM Entries JOIN Moods on moods.id = Entries.mood_id

        SELECT 
            e.id as entry_id, 
            e.concept, 
            e.entry, 
            e.mood_id, 
            e.date,
            m.id as mood_id,
            m.label,
            et.id,
            et.tag_id,
            t.id as tag_id,
            t.name as tag_name
        FROM Entries e
        JOIN Moods m
            ON e.mood_id = m.id
        LEFT JOIN Entry_Tags et 
            ON et.entry_id = e.id
        LEFT JOIN Tags t
            ON t.id = et.tag_id

SELECT * FROM Entry_Tags

        SELECT 
            t.id,
            t.name,
            et.entry_id
        FROM Tags t
        JOIN Entry_tags et
            ON et.tag_id = t.id