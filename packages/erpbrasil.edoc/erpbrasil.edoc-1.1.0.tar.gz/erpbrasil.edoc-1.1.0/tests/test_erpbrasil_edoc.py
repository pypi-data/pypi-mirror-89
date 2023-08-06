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

VALID_CSTAT_LIST = ['137', '138']


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

        self.chave = os.environ.get(
            'chNFe', '35200309091076000144550010001807401003642343'
        )

        session = Session()
        session.verify = False

        transmissao = TransmissaoMDE(self.certificado, session)
        self.mde = MDe(
            transmissao, '35',
            versao='1.01', ambiente='1'
        )

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/test_ultimo_nsu.yaml')
    def test_ultimo_nsu(self):

        ret = self.mde.consultar_distribuicao(
            cnpj_cpf=self.certificado.cnpj_cpf,
            ultimo_nsu='1'.zfill(15),
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/test_nsu_especifico.yaml')
    def test_nsu_especifico(self):

        ret = self.mde.consultar_distribuicao(
            cnpj_cpf=self.certificado.cnpj_cpf,
            nsu_especifico='1'.zfill(15),
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)

    @vcr.use_cassette('tests/fixtures/vcr_cassettes/test_chave.yaml')
    def test_chave(self):

        ret = self.mde.consultar_distribuicao(
            cnpj_cpf=self.certificado.cnpj_cpf,
            chave=self.chave
        )

        self.assertIn(ret.resposta.cStat, VALID_CSTAT_LIST)


t = Tests()
t.setUp()
t.test_ultimo_nsu()
t.test_nsu_especifico()
t.test_chave()
