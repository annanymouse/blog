import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser
#Sfrom splinter.exceptions import ElementDoesNotExist
#from selenium import webdriver

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    def testLoginCorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def testLoginIncorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")
    
    
    def testAddEditPost(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.browser.visit('http://127.0.0.1:5000/post/add')
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/add")
        self.browser.fill("title", "First Post")
        self.browser.fill("content", "Hello World!")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.browser.click_link_by_text('Edit Post')
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1/edit")
        self.browser.fill("title", "Edited First Post")
        self.browser.fill("content", "Hello Universe!")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.assertEqual(self.browser.find_by_tag('h1').first.value, "Edited First Post")
        #divs = self.browser.find_by_tag("div")
        #myList = []
        #if "Hello Universe!" in divs:
            #myList.append("Hello Universe!")
        #self.assertEqual(myList[0], "Hello Universe!")
    
    def testAddDeletePost(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.browser.visit('http://127.0.0.1:5000/post/add')
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/add")
        self.browser.fill("title", "First Post")
        self.browser.fill("content", "Hello World!")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.browser.click_link_by_text('Delete Post')
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/post/1/delete")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")
        self.assertEqual(len(self.browser.find_by_tag('h1')),0)
        #divs = self.browser.find_by_tag("div")
        #myList = []
        #if "Hello Universe!" in divs:
            #myList.append("Hello Universe!")
        #self.assertEqual(myList[0], "Hello Universe!")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()