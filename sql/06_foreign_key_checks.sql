-- Fails: there is no user 99, so the foreign key rejects the row
INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
VALUES ('add', 1, 1, 2, 99);

-- Count calculations per user (the "many" side of one-to-many)
SELECT u.username, COUNT(c.id) AS calculation_count
FROM users u
LEFT JOIN calculations c ON c.user_id = u.id
GROUP BY u.username;