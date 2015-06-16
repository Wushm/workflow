#coding=utf-8
from django import template

register = template.Library()

def filter_record(record, data):
    if data == 'mrs':
        return record.mrs
    if data == 'submitter':
        return record.submitter
    if data == 'reviewer1':
        return record.reviewer1
    if data == 'reviewer2':
        return record.reviewer2
    if data == 'reviewer3':
        return record.reviewer3
    if data == 'totalTime':
        return record.totalTime
    if data == 'mrRootCause':
        return record.mrRootCause
    if data == 'reasonDecription':
        return record.reasonDecription
    if data == 'typicalQuestion':
        return record.typicalQuestion
    if data == 'questionDecr':
        return record.questionDecr
    if data == 'questionNum':
        return record.questionNum
    if data == 'isLeadInto':
        return record.isLeadInto
    if data == 'risk':
        return record.risk
    if data == 'module':
        return record.module
    if data == 'team':
        return record.team
    if data == 'reviewTime':
        return record.reviewTime
    if data == 'reviewer2_energy':
        return record.reviewer2_energy
    if data == 'reviewer3_energy':
        return record.reviewer3_energy
    if data == 'DefectTarget':
        return record.DefectTarget
    if data == 'DefectType':
        return record.DefectType
    if data == 'DefectQualifier':
        return record.DefectQualifier
    if data == 'DefectSource':
        return record.DefectSource
    if data == 'DefectAge':
        return record.DefectAge
    
register.filter('filter_record', filter_record)