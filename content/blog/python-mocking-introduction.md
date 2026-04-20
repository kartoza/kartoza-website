---
author: Zulfikar Akbar Muzakki
date: '2021-01-03'
description: Mocking is a process in unit testing when the test has external dependencies.
  We isolate our code during the test, without having to worry
erpnext_id: /blog/python/python-mocking-introduction
erpnext_modified: '2021-01-03'
reviewedBy: Automated Check
reviewedDate: '2026-04-13'
tags:
- Python
thumbnail: /img/blog/placeholder.png
title: Python Mocking Introduction
---

Mocking is a process in unit testing when the test has external dependencies. We isolate our code during the test, without having to worry about the unexpected behavior of the dependencies. For example, we create a routine to save something to Firebase which utilizes 3rd party library called Firestore. There could be problems when saving data to Firebase, like internet connections, wrong configuration, non-existing document, you name it. Instead of testing every possible scenario when saving to Firebase, we only test that Firestore is called with correct parameter, which represents our data. The tests for Firestore itself should have been done by Firestore developer. Hence, we can shift our focus towards the implementation of our code. It also reduces testing time because we don’t need to send our data to Firebase.

Starting from Python 3.3, `unittest` library includes a subpackage named [`unittest.mock`](<https://docs.python.org/3/library/unittest.mock.html>) which provides useful functions to mock a function/class. Python of previous versions can also install it from _<https://pypi.python.org/pypi/mock>._

Let’s say we have this function to save into Firebase in a file named _**save_firebase.py**_
    
    
    from datetime import date  
    from firebase_admin import firestore  
      
    class SaveGrowthToFirebase():  
      
        def __init__(self, farm_id):  
            self.farm_id = farm_id  
      
        def get_previous_value(self):  
            """  
            Get Growth value of previous date.  
            :return: previous Growth value  
            """  
      
            prev_value = 1  
            # implementation of code to get previous date's Growth value.  
            # We will not go into the implementation detail, because we will  
            # mock it in the test.  
            # ..... <code to get the prev_value> .....  
            return prev_value  
      
        def save_growth_to_firebase(self, collection, document, growth_size) -> None:  
            """  
            Save growth data to Firebase  
            :param growth_size: Size of the crop in cm  
            :return: None  
            """  
            data = {  
                'date': date.today().strftime('%Y-%m-%d'),  
                'growth': growth_size,  
                'changes': growth_size/self.get_previous_value()*100  
            }  
            db = firestore.client(  
                app=self.get_firebase_app()  
            )  
            farm_doc = db.collection(collection).document(document)  
            farm_doc.set(data)  
      
        def get_firebase_app(self):  
            """  
            Get the Firebase app.  
            :return: Firebase App object  
            """  
            FIREBASE_APP = None  
            # implementation of code to get Firebase App.  
            # We will not go into the implementation detail, because we will  
            # mock it in the test.  
            # ..... <code to get the FIREBASE_APP> .....  
            return FIREBASE_APP

Then we have this test case inside **test_save_firebase.py** , without mock _:_
    
    
    from unittest import main, mock, TestCase  
    from datetime import date  
    from save_firebase import SaveGrowthToFirebase  
      
      
    class TestSaveGrowthFirebase(TestCase):  
        """  
        Test saving growth data to Firebase  
        """  
      
        @mock.patch  
        @classmethod  
        def setUpClass(cls):  
            cls.farm_id = 126  
            cls.collection = 'farm-growth'  
            cls.document = str(cls.farm_id)  
            cls.growth_size = 17  
            cls.date_today = date(2020, 1, 1)  
            cls.prev_growth_val = 8.5  
            cls.data = {  
                'date': cls.date_today.strftime('%Y-%m-%d'),  
                'growth': cls.growth_size,  
                'changes': cls.growth_size / cls.prev_growth_val * 100  
            }  
      
        def test_save(self):  
            # Save to Firebase  
            save_growth_to_firebase(self.collection, self.document, self.growth_size)  
          
            # Check above data exists in Firebase  
            db = firestore.client(app=settings.FIREBASE_APP)  
            farm_doc = db.collection(self.collection).document(self.document)  
            farm_doc = farm_doc.get()  
            self.assertTrue(farm_doc.exists)  
            self.assertEqual(farm_doc.to_dict(), {  
                'date': date.today().strftime('%Y-%n-%d'),  
                'growth': self.growth_size  
            })  
      
        def tearDown(self) -> None:  
            # We need to delete the document so it will not bloat our Firebase space  
            db = firestore.client(app=settings.FIREBASE_APP)  
            farm_doc = db.collection(self.collection).document(self.document)  
            farm_doc.delete()

Our test is pretty simple, but it sends real data into Firebase. This example only uses a small amount of data, but if we send data that has maximum document size of Firebase (1MB) then the test will take much longer to run. We also need to count the real Firebase space consumed by our test. Those problems are only for testing one feature, imagine testing more than 10 features that saves data into Firebase.

## Mocking Date in Python

Now, we will refactor the code above to use `Mock`. Let’s start with the simple one: `date`. Our test calls `date.today` and that value will be varied through each test if it’s done in different day. We want to mock that so it always returns same date value no matter when we run the test. Let’s head to `test_save`() and update it to:
    
    
    @mock.patch('save_firebase.date', autospec=True)  
    def test_save(self, mock_client, mock_get_prev_value, mock_date):  
        # Save to Firebase  
        mock_date.today.return_value = self.date_today  
      
        obj = SaveGrowthToFirebase(self.farm_id)  
        obj.save_growth_to_firebase(  
            self.collection, self.document, self.growth_size  
        )

  


Let’s take a look at the code above. `@mock.patch('save_firebase.date'``)` is used to mock the date function inside **save_firebase.py**. Things to note in mocking is to mock an item where it is used, not where it came from. In our case, we use `@mock.patch('save_firebase.date') `instead of `@mock.patch('datetime.date'``)`. Indeed, `date` comes from `datetime`, but we call it in **save_firebase**. Then, we set `mock_date.today.return_value `to a specific date. Remember that we call `date.today` in `SaveGrowthToFirebase`? Setting `return_value` make sure a mocked object returns something expected. With this update, `date.today()` value in our test will always be `2020-01-01`  


## Mocking get_previous_value()

After mocking date, we will mock `get_previous_value``()`. Update `test_save` into this:
    
    
    @mock.patch('save_firebase.date')  
    @mock.patch.object(SaveGrowthToFirebase, 'get_previous_value')  
    def test_save(self, mock_get_prev_value, mock_date):  
        # Save to Firebase  
        mock_date.today.return_value = date(2020, 1, 1)  
        mock_get_prev_value.return_value = 8.5  
        SaveGrowthToFirebase(self.farm_id).save_growth_to_firebase(  
            self.collection, self.document, self.growth_size  
        )

_  
_

We mock `get_previous_value()` using `mock.patch.object()`. It basically works the same way as `mock.patch()`_._` mock.patch()` takes a string which will be resolved to an object when applying the patch, while __` mock.patch.object()` takes a direct reference _._ This means that `mock.patch()` doesn't require us to import the object before patching, while `mock.patch.object()` requires us to import the module before patching. The latter is easier to use if we already have a reference to the object, as in our case we already import __` SaveGrowthToFirebase` _._

## 

## Python Mocking Pitfalls

Now that we mock multiple functions using decorator, there are several pitfalls:

### Mocking Pitfall 1: Order is Important

When using multiple decorators on our test, order is important. I personally had quite a dificult time when I first learned about using multiple decorators in mocking. Take a look at the above code. We can see that the parameters are matched to the reversed order of decorators (left to right mapped to bottom to top). That is because of [the way Python works with multiple decorator](<https://docs.python.org/2/reference/compound_stmts.html#function-definitions>), so the order of execution would be: `mock_date(mock_get_prev_value(test_save))`.

### Mocking Pitfall 2: False Positive Test Result

`mock` library uses two underlying class: `mock.Mock` and `mock.MagicMock`. Those classes have weakness, in which they always accept method calls and property assignments regardless of the real code implementation. Consider the following case, when we add non-default parameter to `SaveGrowthToFirebase.get_previous_value``()`. 
    
    
    def get_previous_value(self, new_parameter):  
        """  
        Get Growth value of previous date.  
        :return: previous Growth value  
        """  
        ....

___  
_

Running our test would give success result.
    
    
    user@kartoza:~/mock_example$ python3.6 test_save_firebase.py   
    .  
    ----------------------------------------------------------------------  
    Ran 1 test in 0.001s  
    OK

In reality, this should give error because we haven’t supply new parameter when we call `get_previous_value()`.

We can overcome this weakness by setting `autospec=True` to our mock decorator. This will create a functionality equivalent to the provided class/function. So, it will raise exception if it’s used in the wrong way, like having wrong number of arguments. As the real class/function changes, it will break the test and it’s expected. Without autospec, our test will still pass and we will get the wrong idea that our code works correctly.

Our `test_save` code would be:
    
    
    @mock.patch('save_firebase.date', autospec=True)  
    @mock.patch.object(SaveGrowthToFirebase, 'get_previous_value', autospec=True)  
    def test_save(self, mock_get_prev_value, mock_date):  
        # Save to Firebase  
        mock_date.today.return_value = date(2020, 1, 1)  
        mock_get_prev_value.return_value = 8.5  
        SaveGrowthToFirebase(self.farm_id).save_growth_to_firebase(  
            self.collection, self.document, self.growth_size  
        )

And will raise error when we run it:
    
    
    _user@kartoza:~/mock_example$ python3.6 test_save_firebase.py  
     TypeError: missing a required argument: 'new_parameter'  
      
    ----------------------------------------------------------------------  
    Ran 1 test in 0.067s  
    FAILED (errors=1)_

It's now giving an error because it mocks the functionality exactly as it is. Update `SaveGrowthToFirebase` as follows to call `get_previous_value() `with a new parameter, which has value `‘new_parameter’`  

    
    
    def get_previous_value(self, new_parameter):  
        """  
        Get Growth value of previous date.  
        :return: previous Growth value  
        """  
      
        prev_value = 1  
        # implementation of code to get previous date's Growth value.  
        # We will not go into the implementation detail, because we will  
        # mock it in the test.  
        # ..... <code to get the prev_value> .....  
        return prev_value  
      
    def save_growth_to_firebase(self, collection, document, growth_size) -> None:  
        """  
        Save growth data to Firebase  
        :param growth_size: Size of the crop in cm  
        :return: None  
        """  
        data = {  
            'date': date.today().strftime('%Y-%m-%d'),  
            'growth': growth_size,  
            'changes': growth_size/self.get_previous_value('new_parameter')*100  
        }  
        db = firestore.client(  
            app=self.get_firebase_app()  
        )  
        farm_doc = db.collection(collection).document(document)  
        farm_doc.set(data)

And our test should look like this:
    
    
    @mock.patch('save_firebase.date', autospec=True)  
    @mock.patch.object(SaveGrowthToFirebase, 'get_previous_value', autospec=True)  
    def test_save(self, mock_client, mock_get_prev_value, mock_date):  
        # Save to Firebase  
        mock_date.today.return_value = self.date_today  
        mock_get_prev_value.return_value = self.prev_growth_val  
      
        obj = SaveGrowthToFirebase(self.farm_id)  
        obj.save_growth_to_firebase(  
            self.collection, self.document, self.growth_size  
        )  
      
        # test get_previous_value is called with correct parameter  
        mock_get_prev_value.assert_called_once_with(obj, 'new_parameter')

In the above test, we check that `get_previous_value() `is really called with new parameter, which has value `‘new_parameter’` using `mock_get_prev_value.assert_called_once_with(obj, 'new_parameter') `and is only called once. Remember, `get_previous_value()` has 2 parameters: `self` and `new_parameter`, and our code only calls the function once.

## Mocking Firestore Functionality

Now for the final part where we mock Firestore functionality. Update our test to look like this:  

    
    
    from unittest import main, mock, TestCase  
    from datetime import date  
    from save_firebase import SaveGrowthToFirebase  
      
    class TestSaveGrowthFirebase(TestCase):  
        """  
        Test saving growth data to Firebase  
        """  
      
        @classmethod  
        def setUpClass(cls):  
            cls.farm_id = 126  
            cls.collection = 'farm-growth'  
            cls.document = str(cls.farm_id)  
            cls.growth_size = 17  
            cls.date_today = date(2020, 1, 1)  
            cls.prev_growth_val = 8.5  
            cls.data = {  
                'date': cls.date_today.strftime('%Y-%m-%d'),  
                'growth': cls.growth_size,  
                'changes': cls.growth_size/cls.prev_growth_val*100  
            }  
      
        @mock.patch('save_firebase.date', autospec=True)  
        @mock.patch.object(SaveGrowthToFirebase, 'get_previous_value', autospec=True)  
        @mock.patch('save_firebase.firestore.client', autospec=True)  
        def test_save(self, mock_client, mock_get_prev_value, mock_date):  
            # Save to Firebase  
            mock_date.today.return_value = self.date_today  
            mock_get_prev_value.return_value = self.prev_growth_val  
      
            obj = SaveGrowthToFirebase(self.farm_id)  
            obj.save_growth_to_firebase(  
                self.collection, self.document, self.growth_size  
            )  
      
            # test get_previous_value is called with correct parameter  
            mock_get_prev_value.assert_called_once_with(obj, 'new_parameter')  
      
            # test db.collection is called with correct parameter  
            mock_client().collection.assert_called_once_with(self.collection)  
      
            # test db.collection.document is called with correct parameter  
            mock_client().collection().document.assert_called_once_with(self.document)  
      
            # test db.collection.document.set is called with correct parameter  
            mock_client().collection().document().set.assert_called_once_with(self.data)  
      
      
    if __name__ == '__main__':  
        main()

Here, we mock Firestore client and check if it is called with the correct parameter value. 

  * `collection()` should be called `'farm-growth'`
  * `document()` should be called with `'126'``_  
_`
  * `set()` should be called with correct dictionary value.



__

Our **save_firebase.py** final code should now looks like this:
    
    
    from datetime import date  
    from firebase_admin import firestore  
      
    class SaveGrowthToFirebase():  
      
        def __init__(self, farm_id):  
            self.farm_id = farm_id  
      
        def get_previous_value(self, new_parameter):  
            """  
            Get Growth value of previous date.  
            :return: previous Growth value  
            """  
      
            prev_value = 1  
            # implementation of code to get previous date's Growth value.  
            # We will not go into the implementation detail, because we will  
            # mock it in the test.  
            # ..... <code to get the prev_value> .....  
            return prev_value  
      
        def save_growth_to_firebase(self, collection, document, growth_size) -> None:  
            """  
            Save growth data to Firebase  
            :param growth_size: Size of the crop in cm  
            :return: None  
            """  
            data = {  
                'date': date.today().strftime('%Y-%m-%d'),  
                'growth': growth_size,  
                'changes': growth_size/self.get_previous_value('new_parameter')*100  
            }  
            db = firestore.client(  
                app=self.get_firebase_app()  
            )  
            farm_doc = db.collection(collection).document(document)  
            farm_doc.set(data)  
      
        def get_firebase_app(self):  
            """  
            Get the Firebase app.  
            :return: Firebase App object  
            """  
            FIREBASE_APP = None  
            # implementation of code to get Firebase App.  
            # We will not go into the implementation detail, because we will  
            # mock it in the test.  
            # ..... <code to get the FIREBASE_APP> .....  
            return FIREBASE_APP

Finally, run our test and see that it’s working perfectly.
    
    
    user@kartoza:~/mock_example$ python3.6 test_save_firebase.py   
    .  
    ----------------------------------------------------------------------  
    Ran 1 test in 0.007s  
    OK

## Conclusion

Mocking is tricky, yes, but it can definitely help us achieving more efficient tests if used correctly. We need to remember that before mocking our test, we should know the structure and flow of our code. It will make our mocking process easier, because we already knows which part to be mocked. 

Now open your favourite IDE/text editor, and start your test mocking project. Good luck!
