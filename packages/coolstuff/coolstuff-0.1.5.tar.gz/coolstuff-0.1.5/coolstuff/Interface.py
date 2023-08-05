from abc import ABC, abstractmethod

class Interface():

    def __init__(self, model, dataset):
        self.model = model
        self.dataset = dataset
