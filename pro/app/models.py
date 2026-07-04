from django.db import models
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField

# Create your models here.

TIER_LIST = [
    ('C-Tier', 'C-Tier'),
    ('B-Tier', 'B-Tier'),
    ('A-Tier', 'A-Tier'),
    ('S-Tier', 'S-Tier'),
    
]

class ClashOfClan(models.Model):
    username = models.CharField(max_length=255)
    trophies = models.PositiveIntegerField(default=10)
    town_hall_level = models.PositiveIntegerField(default=1)
    war_stars = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.username
    
class Valorant(models.Model):
    game_id = models.CharField(max_length=100)
    kd_ratio = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    rank_tier = models.CharField()
    win_rate = models.FloatField(default=1)
    
    def __str__(self):
        return self.game_id
    
    class Meta:
        verbose_name_plural = 'Valorant'

class GamerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gamer_profile")
    discord_username = models.CharField(default="")
    profile_pic = models.ImageField(upload_to='pfp/', blank=True, null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, default='26.470202829291104,80.2466219093185')
    gender = models.CharField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer Not To Say', 'Prefer Not To Say')
    ])
    tier = models.CharField(choices=TIER_LIST, default='C-Tier')
    valorant_info = models.OneToOneField(Valorant, on_delete=models.SET_NULL, null=True, blank=True)
    clash_of_clans_info = models.OneToOneField(ClashOfClan, on_delete=models.SET_NULL, null=True, blank=True)
    profile_level = models.PositiveIntegerField(default=1)
    profile_score = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    def level_up(self):
        level_requirement = {
            1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 
        }
        
        # Check the score required to level up based on the current level
        required_score = level_requirement.get(self.profile_level)
        
        # Check if the score required for leveling up is met
        if required_score and self.profile_score >= required_score:
            return self.profile_level + 1
        return self.profile_level

    def calculate_tier(self):
        # 1. Start with a baseline score
        score = 0
        
        # 2. Add Valorant performance if it exists
        if self.valorant_info:
            # Formula: (K/D * 50) + (WinRate * 100)
            score += (float(self.valorant_info.kd_ratio) * 50) + (self.valorant_info.win_rate * 100)

        if score > 500:
            return 'S-Tier'
        elif score > 300:
            return 'A-Tier'
        elif score > 150:
            return 'B-Tier'
        else:
            return 'C-Tier'

    def save(self, *args, **kwargs):
        self.tier = self.calculate_tier()
        self.profile_level = self.level_up()
        return super().save(*args, **kwargs)

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    location = PlainLocationField(based_fields=['city'], zoom=7, default='26.470202829291104,80.2466219093185')
    profile_level = models.PositiveIntegerField(default=1)
    profile_score = models.PositiveIntegerField(default=0)
    event_credits = models.PositiveIntegerField(default=50)
    
    

