from functools import wraps
from discord.errors import Forbidden, HTTPException, NotFound
import traceback
import asyncpg
from utils import embed

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
            orig_error = getattr(e, 'original', e)
            error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
            try:
                await self.bot.get_channel(754710116753997876).send(f'{error_msg}')
            except AttributeError:
                await self.get_channel(754710116753997876).send(f'{error_msg}')

            except Exception:
                e = embed.succes(desc=f"{e.__class__.__name__}: {e.args[0]}")
                await self.get_channel(754710116753997876).send(embed=e)
    return wrapped
        
        