
import unittest
import project
import images
import maps
from ..base import drupal
import clean

def main():
    clean.clean()
    drupal.testing()
    
    project.Test.runSuite()
    images.Test.runSuite()
    maps.Test.runSuite()


