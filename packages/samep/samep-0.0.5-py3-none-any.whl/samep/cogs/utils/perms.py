def check(mes, perm):
    if mes.author.id == 386289367955537930:
        return True
    if mes.guild.owner == mes.author:
        return True
    if mes.author.guild_permissions.administrator:
        return True

    elif perm == 'channel':
        if mes.author.guild_permissions.manage_channels:
            return True

    elif perm == 'role':
        if mes.author.guild_permissions.manage_roles:
            return True

    elif perm == 'ban':
        if mes.author.guild_permissions.ban_members:
            return True

    elif perm == 'kick':
        if mes.author.guild_permissions.kick_members:
            return True

    elif perm == 'mes':
        if mes.author.guild_permissions.manage_messages:
            return True

    elif perm == 'move':
        if mes.author.guild_permissions.move_members:
            return True