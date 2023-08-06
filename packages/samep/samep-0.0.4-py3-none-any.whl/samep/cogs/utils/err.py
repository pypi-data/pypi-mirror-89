from functools import wraps
from discord.errors import Forbidden, HTTPException, NotFound
import traceback
import asyncpg

def excepter(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except NotFound:
            pass
        except Forbidden:
            pass
        except HTTPException:
            pass
        except asyncpg.exceptions.UndefinedTableError:
            pass
        except asyncpg.exceptions.UndefinedColumnError:
            pass
        except Exception as e:
            print(traceback.format_exc())
    return wrapped
        
        