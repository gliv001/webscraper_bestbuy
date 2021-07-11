--
-- PostgreSQL database dump
--
-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3
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
-- Name: gpu_availability; Type: TABLE; Schema: public; Owner: georgeliv
--
CREATE TABLE public.gpu_availability (
    id integer NOT NULL,
    name character varying(128),
    model character varying(128),
    sku character varying(128),
    available boolean,
    price numeric(12, 2),
    update_time timestamp without time zone
);
ALTER TABLE public.gpu_availability OWNER TO georgeliv;
--
-- Name: gpu_availability_id_seq; Type: SEQUENCE; Schema: public; Owner: georgeliv
--
CREATE SEQUENCE public.gpu_availability_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE public.gpu_availability_id_seq OWNER TO georgeliv;
--
-- Name: gpu_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: georgeliv
--
ALTER SEQUENCE public.gpu_availability_id_seq OWNED BY public.gpu_availability.id;
--
-- Name: subscribers; Type: TABLE; Schema: public; Owner: georgeliv
--
CREATE TABLE public.subscribers (
    id integer NOT NULL,
    name character varying(128),
    email character varying(128)
);
ALTER TABLE public.subscribers OWNER TO georgeliv;
--
-- Name: subscribers_id_seq; Type: SEQUENCE; Schema: public; Owner: georgeliv
--
CREATE SEQUENCE public.subscribers_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE public.subscribers_id_seq OWNER TO georgeliv;
--
-- Name: subscribers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: georgeliv
--
ALTER SEQUENCE public.subscribers_id_seq OWNED BY public.subscribers.id;
--
-- Name: subscribers_to_url; Type: TABLE; Schema: public; Owner: georgeliv
--
CREATE TABLE public.subscribers_to_url (
    id integer NOT NULL,
    subscriber_id integer,
    url_id integer,
    pattern text
);
ALTER TABLE public.subscribers_to_url OWNER TO georgeliv;
--
-- Name: subscribers_to_url_id_seq; Type: SEQUENCE; Schema: public; Owner: georgeliv
--
CREATE SEQUENCE public.subscribers_to_url_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE public.subscribers_to_url_id_seq OWNER TO georgeliv;
--
-- Name: subscribers_to_url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: georgeliv
--
ALTER SEQUENCE public.subscribers_to_url_id_seq OWNED BY public.subscribers_to_url.id;
--
-- Name: urls; Type: TABLE; Schema: public; Owner: georgeliv
--
CREATE TABLE public.urls (
    id integer NOT NULL,
    url character varying(256),
    short_name character varying(128),
    comment character varying(256)
);
ALTER TABLE public.urls OWNER TO georgeliv;
--
-- Name: TABLE urls; Type: COMMENT; Schema: public; Owner: georgeliv
--
COMMENT ON TABLE public.urls IS 'This table stores all urls';
--
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: georgeliv
--
CREATE SEQUENCE public.urls_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE public.urls_id_seq OWNER TO georgeliv;
--
-- Name: urls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: georgeliv
--
ALTER SEQUENCE public.urls_id_seq OWNED BY public.urls.id;
--
-- Name: gpu_availability id; Type: DEFAULT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.gpu_availability
ALTER COLUMN id
SET DEFAULT nextval('public.gpu_availability_id_seq'::regclass);
--
-- Name: subscribers id; Type: DEFAULT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.subscribers
ALTER COLUMN id
SET DEFAULT nextval('public.subscribers_id_seq'::regclass);
--
-- Name: subscribers_to_url id; Type: DEFAULT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.subscribers_to_url
ALTER COLUMN id
SET DEFAULT nextval('public.subscribers_to_url_id_seq'::regclass);
--
-- Name: urls id; Type: DEFAULT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.urls
ALTER COLUMN id
SET DEFAULT nextval('public.urls_id_seq'::regclass);
--
-- Data for Name: gpu_availability; Type: TABLE DATA; Schema: public; Owner: georgeliv
--
--
-- Data for Name: subscribers; Type: TABLE DATA; Schema: public; Owner: georgeliv
--
--
-- Data for Name: subscribers_to_url; Type: TABLE DATA; Schema: public; Owner: georgeliv
--
--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: georgeliv
--
--
-- Name: gpu_availability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: georgeliv
--
SELECT pg_catalog.setval('public.gpu_availability_id_seq', 1054, true);
--
-- Name: subscribers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: georgeliv
--
SELECT pg_catalog.setval('public.subscribers_id_seq', 1, true);
--
-- Name: subscribers_to_url_id_seq; Type: SEQUENCE SET; Schema: public; Owner: georgeliv
--
SELECT pg_catalog.setval('public.subscribers_to_url_id_seq', 1, true);
--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: georgeliv
--
SELECT pg_catalog.setval('public.urls_id_seq', 1, true);
--
-- Name: gpu_availability gpu_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.gpu_availability
ADD CONSTRAINT gpu_availability_pkey PRIMARY KEY (id);
--
-- Name: subscribers subscribers_pkey; Type: CONSTRAINT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.subscribers
ADD CONSTRAINT subscribers_pkey PRIMARY KEY (id);
--
-- Name: subscribers_to_url subscribers_to_url_pkey; Type: CONSTRAINT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.subscribers_to_url
ADD CONSTRAINT subscribers_to_url_pkey PRIMARY KEY (id);
--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: georgeliv
--
ALTER TABLE ONLY public.urls
ADD CONSTRAINT urls_pkey PRIMARY KEY (id);
--
-- PostgreSQL database dump complete
--