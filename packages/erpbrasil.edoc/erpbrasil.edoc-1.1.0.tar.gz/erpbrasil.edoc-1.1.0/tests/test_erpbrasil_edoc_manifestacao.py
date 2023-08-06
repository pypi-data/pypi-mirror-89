# coding=utf-8

import logging.config
import os
from unittest import TestCase

import vcr
from erpbrasil.assinatura.certificado import Certificado
from requests import Session

from erpbrasil.edoc.mde import MDe
from erpbrasil.edoc.mde import TransmissaoMDE

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

VALID_CSTAT_LIST = ['128']


class Tests(TestCase):
    """ Rodar este teste muitas vezes pode bloquear o seu IP"""

    def setUp(self):
        certificado_nfe_caminho = os.environ.get(
            'certificado_nfe_caminho',
            'test/fixtures/dummy_cert.pfx'
        )
        certificado_nfe_senha = os.environ.get(
            'certificado_nfe_senha', 'dummy_password'
        )
        self.certificado = Certificado(
            certificado_nfe_caminho,
            certificado_nfe_senha
        )
        session = Session()
        session.verify = False

        transmissao = TransmissaoMDE(self.certificado, session)
        self.mde = MDe(
            transmissao, '35',
            versao='1.00', ambiente='1'
        )

        self.chave = os.environ.get(
            'chNFe', '35200309091076000144550010001807401003642343'
        )

    @vcr.use_cassette(
        'tests/fixtures/vcr_cassettes/test_confirmacao_da_operacao.yaml')
    def test_confirmacao_da_operacao(self):
        ret = self.mde.confirmacao_da_operacao(
            chave=self.chave,
            cnpj_cpf=self.certificado.cnpj_cpf
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)

    @vcr.use_cassette(
        'tests/fixtures/vcr_cassettes/test_ciencia_da_operacao.yaml')
    def test_ciencia_da_operacao(self):
        ret = self.mde.ciencia_da_operacao(
            chave=self.chave,
            cnpj_cpf=self.certificado.cnpj_cpf
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)

    @vcr.use_cassette(
        'tests/fixtures/vcr_cassettes/test_desconhecimento_da_operacao.yaml')
    def test_desconhecimento_da_operacao(self):
        ret = self.mde.desconhecimento_da_operacao(
            chave=self.chave,
            cnpj_cpf=self.certificado.cnpj_cpf
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)

    @vcr.use_cassette(
        'tests/fixtures/vcr_cassettes/test_operacao_nao_realizada.yaml')
    def test_operacao_nao_realizada(self):
        ret = self.mde.operacao_nao_realizada(
            chave=self.chave,
            cnpj_cpf=self.certificado.cnpj_cpf
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)


t = Tests()
t.setUp()
t.test_confirmacao_da_operacao()
t.test_ciencia_da_operacao()
t.test_desconhecimento_da_operacao()
t.test_operacao_nao_realizada()
