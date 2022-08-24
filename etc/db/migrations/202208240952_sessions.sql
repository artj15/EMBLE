--migrate:up


CREATE TABLE sessions (
    id bigserial primary key,
    camera_id INTEGER,
    horses_id_start_session integer,
    absolute_start TIMESTAMP,
    horses_id_end_session integer,
    absolute_end TIMESTAMP,
    CONSTRAINT sessions_horses_id_start_session_fkey FOREIGN KEY (horses_id_start_session) REFERENCES horses(id),
    CONSTRAINT sessions_horses_id_end_session_fkey FOREIGN KEY (horses_id_end_session) REFERENCES horses(id)
);

INSERT INTO sessions (camera_id, horses_id_start_session, absolute_start, horses_id_end_session, absolute_end) VALUES (1,308729,'2022-07-31 18:19:02',310723,'2022-08-01 04:01:03');
INSERT INTO sessions (camera_id, horses_id_start_session, absolute_start, horses_id_end_session, absolute_end) VALUES (1,307756,'2022-07-31 16:01:00',308627,'2022-07-31 17:41:01');
INSERT INTO sessions (camera_id, horses_id_start_session, absolute_start, horses_id_end_session, absolute_end) VALUES (2,306643,'2022-07-31 12:58:01',307058,'2022-07-31 15:00:01');
INSERT INTO sessions (camera_id, horses_id_start_session, absolute_start, horses_id_end_session, absolute_end) VALUES (2,305788,'2022-07-31 02:51:00',306335,'2022-07-31 11:32:01');
INSERT INTO sessions (camera_id, horses_id_start_session, absolute_start, horses_id_end_session, absolute_end) VALUES (1,305024,'2022-07-30 23:11:02',305414,'2022-07-31 01:06:02');


--migrate:down


DROP TABLE sessions CASCADE