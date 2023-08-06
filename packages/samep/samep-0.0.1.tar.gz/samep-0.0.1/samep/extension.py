from samep.cogs.event import Event, event_table
from samep.cogs.matching import Matching, matchi_table_, matching_table
from samep.cogs.paneru import Paneru_, paneru_table
from samep.cogs.reaction import Auto_Reaction, auto_reaction_table
from samep.cogs.setting import Setting

def setup(bot):
    bot.add_cog(Event(bot))
    bot.add_cog(Matching(bot))
    bot.add_cog(Paneru_(bot))
    bot.add_cog(Auto_Reaction(bot))
    bot.add_cog(Setting(bot))
    bot.add_table(event_table)
    bot.add_table(matchi_table_)
    bot.add_table(matching_table)
    bot.add_table(paneru_table)
    bot.add_table(auto_reaction_table)