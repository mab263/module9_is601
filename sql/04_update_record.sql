UPDATE calculations
SET result = 6
WHERE id = 1;

-- Verify the change
SELECT * FROM calculations WHERE id = 1;
