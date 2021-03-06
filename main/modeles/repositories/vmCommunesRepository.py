#! /usr/bin/python
# -*- coding:utf-8 -*-
import sys
import ast
from ..entities.vmCommunes import VmCommunes
from sqlalchemy import distinct
from ..entities.vmObservations import VmObservations
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import ast




def getAllCommunes(session):
    req = session.query(distinct(VmCommunes.commune_maj), VmCommunes.insee).all()
    communeList = list()
    for r in req:
        temp = { 'label' : r[0], 'value' : r[1]}
        communeList.append(temp)
    return communeList



def getCommuneFromInsee(connection, insee):
    sql = "SELECT c.commune_maj, \
           c.insee, \
           c.commune_geojson \
           FROM atlas.vm_communes c \
           WHERE c.insee = :thisInsee"
    req = connection.execute(text(sql), thisInsee = insee)
    communeObj = dict()
    for r in req:
        communeObj = {'communeName': r.commune_maj, 'insee': str(r.insee), 'communeGeoJson' : ast.literal_eval(r.commune_geojson)}
    return communeObj


    return req[0].commune_maj



def getCommunesObservationsChilds(connection, cd_ref):
    sql = "select distinct(com.insee) as insee \
    , com.commune_maj \
    FROM atlas.vm_communes com \
    JOIN atlas.vm_observations obs ON obs.insee = com.insee \
    WHERE obs.cd_ref in ( \
    SELECT * from atlas.find_all_taxons_childs(:thiscdref) \
    )OR obs.cd_ref = :thiscdref \
    ORDER BY com.commune_maj ASC".encode('UTF-8')
    req = connection.execute(text(sql), thiscdref = cd_ref)
    listCommunes = list()
    for r in req:
        temp = {'insee': r.insee, 'commune_maj': r.commune_maj}
        listCommunes.append(temp)
    return listCommunes
