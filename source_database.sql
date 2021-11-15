--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Ubuntu 13.4-4.pgdg20.04+1)
-- Dumped by pg_dump version 14.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: club; Type: TABLE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE TABLE public.club (
    _id integer NOT NULL,
    name character varying(100) NOT NULL,
    head character varying(100) NOT NULL,
    category character varying(100) NOT NULL,
    description character varying(100)
);


ALTER TABLE public.club OWNER TO uoaidyfadwrwpe;

--
-- Name: club__id_seq; Type: SEQUENCE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE SEQUENCE public.club__id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.club__id_seq OWNER TO uoaidyfadwrwpe;

--
-- Name: club__id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER SEQUENCE public.club__id_seq OWNED BY public.club._id;


--
-- Name: event; Type: TABLE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE TABLE public.event (
    _id integer NOT NULL,
    name character varying(100) NOT NULL,
    club_id integer NOT NULL,
    visibility character varying(50) NOT NULL,
    start_timestamp timestamp without time zone NOT NULL,
    end_timestamp timestamp without time zone NOT NULL,
    location character varying(100) NOT NULL,
    max_registration integer NOT NULL,
    description character varying(100),
    fee integer NOT NULL,
    status character varying(10) NOT NULL,
    registered_count integer NOT NULL
);


ALTER TABLE public.event OWNER TO uoaidyfadwrwpe;

--
-- Name: event__id_seq; Type: SEQUENCE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE SEQUENCE public.event__id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event__id_seq OWNER TO uoaidyfadwrwpe;

--
-- Name: event__id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER SEQUENCE public.event__id_seq OWNED BY public.event._id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE TABLE public.role (
    student_id integer NOT NULL,
    club_id integer NOT NULL,
    role character varying(20) NOT NULL
);


ALTER TABLE public.role OWNER TO uoaidyfadwrwpe;

--
-- Name: student; Type: TABLE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE TABLE public.student (
    _id integer NOT NULL,
    name character varying(100) NOT NULL,
    email_id character varying(100) NOT NULL,
    college character varying(100) NOT NULL,
    department character varying(100) NOT NULL
);


ALTER TABLE public.student OWNER TO uoaidyfadwrwpe;

--
-- Name: student__id_seq; Type: SEQUENCE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE SEQUENCE public.student__id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student__id_seq OWNER TO uoaidyfadwrwpe;

--
-- Name: student__id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER SEQUENCE public.student__id_seq OWNED BY public.student._id;


--
-- Name: student_event; Type: TABLE; Schema: public; Owner: uoaidyfadwrwpe
--

CREATE TABLE public.student_event (
    student_id integer NOT NULL,
    event_id integer NOT NULL,
    status character varying(100)
);


ALTER TABLE public.student_event OWNER TO uoaidyfadwrwpe;

--
-- Name: club _id; Type: DEFAULT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.club ALTER COLUMN _id SET DEFAULT nextval('public.club__id_seq'::regclass);


--
-- Name: event _id; Type: DEFAULT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.event ALTER COLUMN _id SET DEFAULT nextval('public.event__id_seq'::regclass);


--
-- Name: student _id; Type: DEFAULT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.student ALTER COLUMN _id SET DEFAULT nextval('public.student__id_seq'::regclass);


--
-- Data for Name: club; Type: TABLE DATA; Schema: public; Owner: uoaidyfadwrwpe
--

COPY public.club (_id, name, head, category, description) FROM stdin;
1	kasa	shikha	engineering	blah blah
3	namechange	asrani	engineering	blah blah blah
\.


--
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: uoaidyfadwrwpe
--

COPY public.event (_id, name, club_id, visibility, start_timestamp, end_timestamp, location, max_registration, description, fee, status, registered_count) FROM stdin;
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: uoaidyfadwrwpe
--

COPY public.role (student_id, club_id, role) FROM stdin;
2	1	member
2	3	member
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: uoaidyfadwrwpe
--

COPY public.student (_id, name, email_id, college, department) FROM stdin;
1	jajaja	haja	columbia	coms
2	jajaja	haja	columbia	coms
3	jajaja	haja	columbia	coms
\.


--
-- Data for Name: student_event; Type: TABLE DATA; Schema: public; Owner: uoaidyfadwrwpe
--

COPY public.student_event (student_id, event_id, status) FROM stdin;
\.


--
-- Name: club__id_seq; Type: SEQUENCE SET; Schema: public; Owner: uoaidyfadwrwpe
--

SELECT pg_catalog.setval('public.club__id_seq', 4, true);


--
-- Name: event__id_seq; Type: SEQUENCE SET; Schema: public; Owner: uoaidyfadwrwpe
--

SELECT pg_catalog.setval('public.event__id_seq', 1, false);


--
-- Name: student__id_seq; Type: SEQUENCE SET; Schema: public; Owner: uoaidyfadwrwpe
--

SELECT pg_catalog.setval('public.student__id_seq', 3, true);


--
-- Name: club club_pkey; Type: CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.club
    ADD CONSTRAINT club_pkey PRIMARY KEY (_id);


--
-- Name: event event_pkey; Type: CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (_id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (student_id, club_id);


--
-- Name: student_event student_event_pkey; Type: CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.student_event
    ADD CONSTRAINT student_event_pkey PRIMARY KEY (student_id, event_id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (_id);


--
-- Name: event event_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_club_id_fkey FOREIGN KEY (club_id) REFERENCES public.club(_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: role role_club_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_club_id_fkey FOREIGN KEY (club_id) REFERENCES public.club(_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: role role_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: student_event student_event_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.student_event
    ADD CONSTRAINT student_event_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: student_event student_event_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uoaidyfadwrwpe
--

ALTER TABLE ONLY public.student_event
    ADD CONSTRAINT student_event_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: uoaidyfadwrwpe
--

REVOKE ALL ON SCHEMA public FROM postgres;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO uoaidyfadwrwpe;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO uoaidyfadwrwpe;


--
-- PostgreSQL database dump complete
--

