import os
from itertools import product
from multiprocessing import Pool

import pandas as pd

from phenopy import generate_annotated_hpo_network
from phenopy.config import config
from phenopy.score import Scorer

    def __init__(self, hpo_network, summarization_method='BMWA', min_score_mask=0.05,
                 scoring_method='HRSS'):
        self.hpo_network = hpo_network
        if summarization_method not in ['BMA', 'BMWA', 'maximum']:
            raise ValueError('Unsupported summarization method, please choose from BMA, BMWA, or maximum.')
        self.summarization_method = summarization_method
        self.min_score_mask = min_score_mask
        if scoring_method not in ['HRSS', 'Resnik', 'Jaccard', 'word2vec']:
            raise ValueError('Unsupported semantic similarity scoring method, please choose from HRSS, Resnik, Jaccard, or word2vec.')
        self.scoring_method = scoring_method
        if scoring_method == 'word2vec':
            try:
                self.word_vectors = gensim.models.KeyedVectors.load(config.get('models', 'phenopy.wv.model'))
            except FileNotFoundError:
                raise ValueError("Please make sure that a word2vec model is in your project data directory.")

class MultiScorer:

    def __init__(self, ) -> None:
        # data directory
        
        # phenopy_data_directory = os.path.join(os.getenv("HOME"), ".phenopy/data")

        # files used in building the annotated HPO network
        self.obo_file = config.get('hpo', 'obo_file')
        self.disease_to_phenotype_file_hpoa = config.get('hpo', 'disease_to_phenotype_file')
        self.disease_to_phenotype_file_lit = os.path.join(
            phenopy_data_directory, "custom_ann_file_lit.tsv"
        )
        self.disease_to_phenotype_file_dipr = os.path.join(
            phenopy_data_directory, "custom_ann_file.tsv"
        )
        try:
            self.word_vectors = gensim.models.KeyedVectors.load(config.get('models', 'phenopy.wv.model'))
        except FileNotFoundError:
            raise ValueError("Please make sure that a word2vec model is in your project data directory.")

        # hpoa objects
        (
            self.hpo_network_hpoa,
            self.alt2prim_hpoa,
            self.disease_records_hpoa,
        ) = generate_annotated_hpo_network(
            self.obo_file,
            self.disease_to_phenotype_file_hpoa,
        )
        # lit objects
        (
            self.hpo_network_lit,
            self.alt2prim_lit,
            self.disease_records_lit,
        ) = generate_annotated_hpo_network(
            self.obo_file,
            self.disease_to_phenotype_file_lit,
        )
        # dipr objects
        (
            self.hpo_network_dipr,
            self.alt2prim_dipr,
            self.disease_records_dipr,
        ) = generate_annotated_hpo_network(
            self.obo_file,
            self.disease_to_phenotype_file_dipr,
        )

        # phenopy scorer objects
        self.hrss_hpoa = Scorer(self.hpo_network_hpoa, scoring_method="HRSS")
        self.hrss_lit = Scorer(self.hpo_network_lit, scoring_method="HRSS")
        self.hrss_dipr = Scorer(self.hpo_network_dipr, scoring_method="HRSS")

        self.jaccard_lit = Scorer(self.hpo_network_lit, scoring_method="Jaccard")
        self.jaccard_dipr = Scorer(self.hpo_network_dipr, scoring_method="Jaccard")

        self.w2v_lit = Scorer(self.hpo_network_lit, scoring_method="word2vec")
        self.w2v_dipr = Scorer(self.hpo_network_dipr, scoring_method="word2vec")

        # miscellaneous objects 
        mim2gene = pd.read_pickle(os.path.join(phenopy_data_directory, 'mim2gene.pkl'))
        self.mim2gene = dict(zip(mim2gene['mim_number'].astype(str), mim2gene['Approved symbol']))


    def score_all(self, ):
        
