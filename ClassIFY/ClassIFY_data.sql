-- Subjects
INSERT INTO subjects (SubjectCode, Name, Instructor, Units, Goals) VALUES
('CS 212', 'Computer Organization with Assembly Language', 'DELA CRUZ, MAURICE OLIVER Y.', 3, 'Learn how assembler and compiler works'),
('GEd 109', 'Science, Technology and Society', 'MAGADIA, GLEN FERDINAND C.', 3, 'Defend the research project!'),
('CS 211', 'Object-Oriented Programming', 'AGDON, FATIMA MARIE P.', 3, 'Learn more about OOP Java and able to apply on some projects'),
('PATHFit 3', 'Traditional and Recreational Games', 'DE CASTRO, JOEY R.', 3, 'Learn how to play table tennis and have a healthy lifestyle'),
('Phy 101', 'Calculus-Based Physics', 'MENDOZA, BABY KAREN L.', 3, 'Understand all the lessons'),
('CpE 405', 'Discrete Mathematics', 'BAGSIT, CHARLES CONRAD P.', 3, 'Learn more about logics with math!'),
('IT 212', 'Computer Networking 1', 'MACATANGAY, LLOYD H.', 3, 'Get CISCO NetAcad certification');

-- Tasks
INSERT INTO tasks (SubjectCode, TaskName, Deadline, Priority, Status) VALUES
('CpE 405', 'Review for final exam', '2025-12-12', 'High', 'Not Started'),
('CS 211', 'Review for final exam', '2025-12-09', 'High', 'Not Started'),
('CS 211', 'Review for quiz', '2025-12-09', 'High', 'In Progress'),
('CS 212', 'Review for final exam 
 and practice coding with assembly language', '2025-12-11', 'High', 'Not Started'),
('Phy 101', 'Successfully defend the research project in Physics and STS', '2025-12-04', 'High', 'Completed');

-- Schedule
INSERT INTO schedule (SubjectCode, Day, StartTime, EndTime, Room) VALUES
('Phy 101', 'Mon', '10:00', '13:00', 'ROOM 402'),
('GEd 109', 'Mon', '14:00', '17:00', 'ROOM 101'),
('CS 211', 'Tue', '07:00', '10:00', 'LAB 02'),
('Phy 101', 'Tue', '11:00', '13:00', 'ROOM 105'),
('IT 212', 'Wed', '10:00', '13:00', 'LAB 06'),
('PATHFit 3', 'Wed', '14:00', '16:00', 'GYM'),
('CS 211', 'Thu', '07:00', '09:00', 'ONLINE'),
('IT 212', 'Thu', '14:00', '16:00', 'ONLINE'),
('CS 212', 'Thu', '11:00', '13:00', 'ONLINE'),
('CS 212', 'Fri', '07:00', '10:00', 'LAB 03'),
('CpE 405', 'Sat', '07:00', '10:00', 'ROOM 103');
