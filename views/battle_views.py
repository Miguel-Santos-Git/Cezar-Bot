import discord

class start_battle_view(discord.ui.View):
    def __init__(self,monster, plr_id):
        super().__init__()

        self.plr_id = plr_id
        self.monster = monster
        self.used = False


    @discord.ui.button(label="Accept Battle ",style=discord.ButtonStyle.green)
    async def accept_click(self,interaction: discord.Interaction, button):
        if self.plr_id != interaction.user.id:
            await interaction.response.send_message("You aren't owner of this battle!",ephemeral=True)
            return

        if self.used: return
        self.used = True

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

        await interaction.followup.send("The Battle is starting...")

    @discord.ui.button(label="Decline Battle ",style=discord.ButtonStyle.danger)
    async def decline_click(self,interaction: discord.Interaction, button):
        if self.plr_id != interaction.user.id:
            await interaction.response.send_message("You aren't owner of this battle!",ephemeral=True)
            return
        
        if self.used: return
        self.used = True

        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)

        await interaction.followup.send("The Battle is cancel...")