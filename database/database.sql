-- create database DiseasepredictionDB;
-- --------------------------------------------------------
use DiseasepredictionDB;

-- Table structure for table `user_information`

-- CREATE TABLE `user_information` (
--   `id` int(11) NOT NULL,
--   `first_name` varchar(255) NOT NULL,
--   `last_name` varchar(255) NOT NULL,
--   `age` varchar(255) NOT NULL,
--   `gender` varchar(255) NOT NULL,
--   `city` varchar(255) NOT NULL,
--   `address` varchar(255) NOT NULL,
--   `username` varchar(255) NOT NULL,
--   `password` varchar(255) NOT NULL,
--   `phone_number` varchar(255) NOT NULL
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -- Dumping data for table `user_information`

-- INSERT INTO `user_information` (`id`, `first_name`, `last_name`, `age`, `gender`, `city`, `address`, `username`, `password`,`phone_number`) VALUES
-- (14, 'Mohammed', 'Taheer', '22', 'Male', 'Chintamani', 'Tankbund Road ', 'Taheer', 'Taheer@123', '9008154695');

-- ALTER TABLE `user_information`
--   ADD PRIMARY KEY (`id`);

-- -- AUTO_INCREMENT for table `user_information`
-- ALTER TABLE `user_information`
--   MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

-- -- - ---- --  patient_info -- --- ------

-- CREATE TABLE `patient_info` (
--   `id_2` int NOT NULL AUTO_INCREMENT,
--   `full_name` varchar(255) NOT NULL,
--   `age` varchar(255) NOT NULL,
--   `gender` varchar(255) NOT NULL,
--   `id` int(11) NOT NULL,
--   `patient_date` DATE NOT NULL,
--   `patient_time` TIME NOT NULL,
--   PRIMARY KEY (id_2),
--   FOREIGN KEY (id) REFERENCES user_information (id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
-- ALTER TABLE `patient_info` AUTO_INCREMENT=5000;

-- INSERT INTO `patient_info` (`full_name`, `age`, `gender`, `id`, `patient_date`, `patient_time`) 
-- VALUES('kireeti', '20', 'Male',14,'2021-11-07', '07:19:20');

-- -- - ---- --  sym_dis -- --- ------

-- CREATE TABLE `sym_dis` (
--   `id_3` int NOT NULL AUTO_INCREMENT,
--   `id_2` int NOT NULL,
--   `symptom_1` varchar(255) NOT NULL,
--   `symptom_2` varchar(255) NOT NULL,
--   `symptom_3` varchar(255) NOT NULL,
--   `symptom_4` varchar(255) NOT NULL,
--   `symptom_5` varchar(255) NOT NULL,
--   `disease` varchar(255) NOT NULL,
--   `sym_date` DATE NOT NULL,
--   `sym_time` TIME NOT NULL,
-- 	PRIMARY KEY (id_3,id_2),
--     FOREIGN KEY (id_2) REFERENCES patient_info (id_2)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 
-- ALTER TABLE `sym_dis` AUTO_INCREMENT=10000;

-- INSERT INTO `sym_dis` (`id_2`, `symptom_1`, `symptom_2`, `symptom_3`, `symptom_4`,`symptom_5`,`disease`, `sym_date`, `sym_time`) 
-- VALUES (5000, 'skin_rash', 'passage_of_gases', 'lack_of_concentration', 'None','None','Acne', '2021-11-07', '08:19:20');

select * from user_information;
select * from patient_info;
select * from sym_dis;

-- -- showing user entered "patient names" and "all the preicted diseases"  
select p.full_name, s.symptom_1, s.symptom_2, s.symptom_3, s.symptom_4, s.symptom_5, s.disease from patient_info p, sym_dis s where p.id_2 = s.id_2 and p.id = 15;
