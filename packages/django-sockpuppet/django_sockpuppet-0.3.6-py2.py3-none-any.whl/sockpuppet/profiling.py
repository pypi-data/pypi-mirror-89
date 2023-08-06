
import cProfile
from django.utils.decorators import method_decorator
# https://stackoverflow.com/questions/5375624/a-decorator-that-profiles-a-method-call-and-logs-the-profiling-result
# https://docs.djangoproject.com/en/2.2/_modules/django/utils/decorators/
# pip install snakeviz
# snakeviz profile_file

def profileit(name):
    def inner(func):
        def wrapper(*args, **kwargs):
            prof = cProfile.Profile()
            retval = prof.runcall(func, *args, **kwargs)
            # Note use of name from outer scope
            prof.dump_stats(name)
            return retval
        return wrapper
    return inner

profile_method = method_decorator(profileit)
