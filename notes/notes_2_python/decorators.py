def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with the function")

        return wrapper

# input f in 'announce(f)' -> 'hello()'
@announce
def hello():
  print("Hello, world!")
  
hello()