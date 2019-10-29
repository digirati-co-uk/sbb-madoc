LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (email, name, created, modified, password_hash, role, is_active) VALUES ('admin@example.org', 'admin', '2019-10-29 09:55:54', '2019-10-29 09:55:54', '$2y$10$Tp8k0V0pNfchUXMJArJN/eIXZuFRpX9BpxaKPgP213htMnjMkNtj.', 'global_admin', 1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
