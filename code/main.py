import discord
import requests
import os
import bot_variables
intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)

tempUnit = "c"
wrongCity = 1  # 1=wrong
def temperatureColor(temperature, ):
    unit = tempUnit
    if ((temperature < 11 and unit == 'c')
        or (temperature < 51.8 and unit == 'f')
            or (temperature < 284.15 and unit == 'k')):
        return temperatureColors["<10"]
    elif ((temperature >= 11 and temperature < 21 and unit == 'c')
          or (temperature >= 51.8 and temperature < 69.8 and unit == 'f')
          or (temperature >= 284.15 and temperature < 293.15 and unit == 'k')):
        return temperatureColors["11-20"]
    elif ((temperature >= 21 and temperature < 26 and unit == 'c')
          or (temperature >= 69.8 and temperature < 78.8 and unit == 'f')
          or (temperature >= 293.15 and temperature < 302.15 and unit == 'k')):
        return temperatureColors["21-25"]
    elif ((temperature >= 26 and temperature < 31 and unit == 'c')
          or (temperature >= 78.8 and temperature < 87.8 and unit == 'f')
          or (temperature >= 302.15 and temperature < 311.15 and unit == 'k')):
        return temperatureColors["26-30"]
    elif ((temperature >= 31 and temperature < 36 and unit == 'c')
          or (temperature >= 87.8 and temperature < 96.8 and unit == 'f')
          or (temperature >= 311.15 and temperature < 320.15 and unit == 'k')):
        return temperatureColors["31-35"]
    elif ((temperature >= 36 and temperature < 41 and unit == 'c')
          or (temperature >= 96.8 and temperature < 105.8 and unit == 'f')
          or (temperature >= 320.15 and temperature < 329.15 and unit == 'k')):
        return temperatureColors["36-40"]
    elif ((temperature >= 41 and temperature < 46 and unit == 'c')
          or (temperature >= 105.8 and temperature < 114.8 and unit == 'f')
          or (temperature >= 329.15 and temperature < 338.15 and unit == 'k')):
        return temperatureColors["41-45"]
    else:
        return temperatureColors["46<"]


def timezone(time):
    secs = int((time % 3600) / 60)
    if (secs == 0):
        secs = "00"
    return f"UTC + {int(time/3600)}:{secs}"


def Data(city):
    api_key = ""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def help():
    embed = discord.Embed(
        title="Here To Help!",
        description="I'm a weather bot built by Shoubhit Jamadhiar.\nI can display current weather information for a given city!\nUse `w!command <command_name>` to get more information on a specific command",
        color=discord.Color.random())

    embed.add_field(name="`w!getAll <city_name>`",
                    value="Get all the information for a city.",
                    inline=False)
    embed.add_field(name="`w!getLoc <city_name>`",
                    value="Get the location details of a city.",
                    inline=False)
    embed.add_field(name="`w!getTemp <city_name>`",
                    value="Get the temperature information of a city.",
                    inline=False)
    embed.add_field(name="`w!getAtm <city_name>`",
                    value="Get the atmospheric information of a city.",
                    inline=False)
    embed.add_field(name="`w!getWeather <city_name>`",
                    value="Get the weather information of a city.",
                    inline=False)
    embed.add_field(
        name="`w!get <city_name> <field1, field2, ...>`",
        value="Get specific weather information for a city. Specify the required fields to display.",
        inline=False)
    embed.add_field(
        name="`w!convert <unit>`",
        value="Convert temperature unit to Celsius (c), Fahrenheit (f), or Kelvin (k).",
        inline=False)
    embed.add_field(
        name="Note",
        value="* Angular brackets are just for syntax purposes\n* None of these commands are case sensitive",
        inline=False)
    return embed


def getAll(city):
    data = Data(city)
    city = city.title()
    print(f"{city}'s data:", data)
    country = data["sys"]["country"]
    weatherID = data['weather'][0]['id']
    print(f"Tempunit is now {tempUnit}")

    if (tempUnit == 'c'):
        current = f"{data['main']['temp']} °C"
        minimum = f"{data['main']['temp_min']} °C"
        maximum = f"{data['main']['temp_max']} °C"
        forecast = f"{data['main']['feels_like']} °C"
    if (tempUnit == 'f'):
        current = f"{int(data['main']['temp']) * 9/5 + 32} °F"
        minimum = f"{int(data['main']['temp_min']) * 9/5 + 32} °F"
        maximum = f"{int(data['main']['temp_max']) * 9/5 + 32} °F"
        forecast = f"{int(data['main']['feels_like']) * 9/5 + 32} °F"
    if (tempUnit == 'k'):
        current = f"{int(data['main']['temp']) + 273.15} K"
        minimum = f"{int(data['main']['temp_min']) + 273.15} K"
        maximum = f"{int(data['main']['temp_max']) + 273.15} K"
        forecast = f"{int(data['main']['feels_like']) + 273.15} K"

    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by Openweather",
        color=weatherColors[weatherID])
    embed.add_field(
        name="Location",
        value=f"Longitude : `{data['coord']['lon']}°`\nLatitude : `{data['coord']['lat']}°`\nTimezone : `{timezone(data['timezone'])}`",
        inline=False)
    embed.add_field(
        name="Temperature",
        value=f"Current : `{current}`\nMinimum : `{minimum}`\nMaximum : `{maximum}`\nForecast : `{forecast}`",
        inline=False)
    embed.add_field(
        name="Atmosphere",
        value=f"Pressure : `{data['main']['pressure']} hPa`\nHumidity : `{data['main']['humidity']}%`\nVisibility : `{data['visibility']} m`",
        inline=False)
    embed.add_field(
        name="Weather",
        value=f"Weather : `{data['weather'][0]['description'].title( )}`\nWind : `{data['wind']['speed']} m/s`",
        inline=False)
    return embed


def get(city, specify):
    global wrongCity
    wrongCity = 1
    data = Data(city)
    if (data == None):
        return
    wrongCity = 0
    city = city.title()
    print(f"{city}'s data:", data)
    country = data["sys"]["country"]
    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by OpenWeatherMap",
        color=discord.Color.dark_grey())
    if (tempUnit == 'c'):
        current = f"{data['main']['temp']} °C"
        minimum = f"{data['main']['temp_min']} °C"
        maximum = f"{data['main']['temp_max']} °C"
        forecast = f"{data['main']['feels_like']} °C"
    if (tempUnit == 'f'):
        current = f"{int(data['main']['temp']) * 9/5 + 32} °F"
        minimum = f"{int(data['main']['temp_min']) * 9/5 + 32} °F"
        maximum = f"{int(data['main']['temp_max']) * 9/5 + 32} °F"
        forecast = f"{int(data['main']['feels_like']) * 9/5 + 32} °F"
    if (tempUnit == 'k'):
        current = f"{int(data['main']['temp']) + 273.15} K"
        minimum = f"{int(data['main']['temp_min']) + 273.15} K"
        maximum = f"{int(data['main']['temp_max']) + 273.15} K"
        forecast = f"{int(data['main']['feels_like']) + 273.15} K"
    if (specify == []):
        embed.add_field(name="Error",
                        description="You need to have a minimum of 1 field",
                        inline=False)
    elif (len(specify) > 12):
        embed.add_field(name="Error",
                        value="Please specify a maximum of 12 fields",
                        inline=False)
    else:
        for i in specify:
            i = i.lower()
            i = i.strip()
            if (i == "longitude"):
                embed.add_field(name="Longitude",
                                value=f"`{data['coord']['lon']}°`",
                                inline=True)
            elif (i == "latitude"):
                embed.add_field(name="Latitude",
                                value=f"`{data['coord']['lat']}°`",
                                inline=True)
            elif (i == "timezone"):
                embed.add_field(name="Timezone",
                                value=f"`{timezone(data['timezone'])}`",
                                inline=True)
            elif (i == "curr" or i == "current" or i == "currtemp"
                  or i == "currenttemperature" or i == "current temperature"):
                embed.add_field(name="Current Temperature",
                                value=f"`{current}`",
                                inline=True)
            elif (i == "min" or i == "minimum" or i == "mintemp"
                  or i == "minimumtemperature" or i == "minimum temperature"):
                embed.add_field(name="Minimum Temperature",
                                value=f"`{minimum}`",
                                inline=True)
            elif (i == "max" or i == "maximum" or i == "maxtemp"
                  or i == "maximumtemperature" or i == "maximum temperature"):
                embed.add_field(name="Maximum Temperature",
                                value=f"`{maximum}`",
                                inline=True)
            elif (i == "forecast" or i == "predicted temperature"
                  or i == "predictedtemperature" or i == "forecasted temperature"
                  or i == "forecastedtemperature"):
                embed.add_field(name="Temperature Forecast",
                                value=f"`{forecast}`",
                                inline=True)
            elif (i == "pressure"):
                embed.add_field(name="Atmospheric Pressure",
                                value=f"`{data['main']['pressure']} hPa`",
                                inline=True)
            elif (i == "humidity"):
                embed.add_field(name="Humidity",
                                value=f"`{data['main']['humidity']}%`",
                                inline=True)
            elif (i == "visibility"):
                embed.add_field(name="Visibility",
                                value=f"`{data['visibility']} m`",
                                inline=True)
            elif (i == "weather"):
                embed.add_field(
                    name="Weather",
                    value=f"`{data['weather'][0]['description'].title( )}`",
                    inline=True)
            elif (i == "windspeed"):
                embed.add_field(name="Wind Speed",
                                value=f"`{data['wind']['speed']} m/s`",
                                inline=True)
            else:
                embed.add_field(name="Error",
                                value=f"`{i}` is not a valid field",
                                inline=True)
    return embed


def getLoc(city):
    data = Data(city)
    city = city.title()
    print(f"{city}'s data:", data)
    country = data["sys"]["country"]
    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by OpenWeatherMap",
        color=discord.Color.dark_grey())
    embed.add_field(
        name="Location",
        value=f"Latitude : `{data['coord']['lat']}°`\nLongitude : `{data['coord']['lon']}°`\nTimezone : `{timezone(data['timezone'])}`",
        inline=False)
    return embed


def getTemp(city):
    data = Data(city)
    city = city.title()
    print(f"{city}'s data:", data)
    country = data["sys"]["country"]
    color = temperatureColor(data['main']['temp'])

    if (tempUnit == 'c'):
        current = f"{data['main']['temp']} °C"
        minimum = f"{data['main']['temp_min']} °C"
        maximum = f"{data['main']['temp_max']} °C"
        forecast = f"{data['main']['feels_like']} °C"
    if (tempUnit == 'f'):
        current = f"{int(data['main']['temp']) * 9/5 + 32} °F"
        minimum = f"{int(data['main']['temp_min']) * 9/5 + 32} °F"
        maximum = f"{int(data['main']['temp_max']) * 9/5 + 32} °F"
        forecast = f"{int(data['main']['feels_like']) * 9/5 + 32} °F"
    if (tempUnit == 'k'):
        current = f"{int(data['main']['temp']) + 273.15} K"
        minimum = f"{int(data['main']['temp_min']) + 273.15} K"
        maximum = f"{int(data['main']['temp_max']) + 273.15} K"
        forecast = f"{int(data['main']['feels_like']) + 273.15} K"

    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by Openweather",
        color=color)
    embed.add_field(
        name="Temperature",
        value=f"Current : `{current}`\nMinimum : `{minimum}`\nMaximum : `{maximum}`\nForecast : `{forecast}`",
        inline=False)
    return embed


def getAtm(city):
    data = Data(city)
    city = city.title()
    print(f"{city}'s data:", data)
    country = data['sys']['country']
    weatherID = data['weather'][0]['id']
    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by Openweather",
        color=weatherColors[weatherID])
    embed.add_field(
        name="Atmosphere",
        value=f"Pressure : `{data['main']['pressure']} hPa`\nHumidity : `{data['main']['humidity']}%`\nVisibility : `{data['visibility']} m`",
        inline=False)
    return embed


def getWeather(city):
    data = Data(city)
    city = city.title()
    print(f"{city}'s data:", data)
    country = data["sys"]["country"]
    weatherID = data['weather'][0]['id']
    embed = discord.Embed(
        title=f"{city.title( )}, {countries[country]}",
        description="The following information has been provided by Openweather",
        color=weatherColors[weatherID])
    embed.add_field(
        name="Weather",
        value=f"Weather : `{data['weather'][0]['main']}`\nWind : `{data['wind']['speed']} m/s`",
        inline=False)
    return embed


@client.event
async def on_ready():
    print(f"Logged into discord as {client.user}")


@client.event
async def on_message(message):

    mes = message.content
    mes = mes.lower()
    global tempUnit

    if (message.author == client.user):
        return

    if (mes.split()[0] == "w!help"):
        embed = help()
        await message.channel.send(embed=embed)
        return

    if (mes.split()[0] == "w!command"):
        command = mes.split()[1]
        command = command.lower()
        embed = discord.Embed(color=discord.Color.random())

        if (command == "w!getall" or command == "getall"):
            embed.title = f"Command: `w!getAll`"
            embed.description = "Displays all the weather, climate, and forecast information for the given city."
            embed.add_field(name="Syntax: `w!getAll <city_name>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!getAll New York`",
                            value="",
                            inline=False)

        if (command == "w!getloc" or command == "getloc"):
            embed.title = f"Command: `w!getLoc`"
            embed.description = "Displays the `latitude`, `longitude`, and `timezone` for the given city."
            embed.add_field(name="Syntax: `w!getLoc <city_name>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!getLoc London`",
                            value="",
                            inline=False)

        if (command == "w!gettemp" or command == "gettemp"):
            embed.title = f"Command: `w!getTemp`"
            embed.description = "Will tell you about the `current temperature`, `minimum temperature`, `maximum temperature`, and `forecast (predicted temp)`for the given city."
            embed.add_field(name="Syntax: `w!getTemp <city_name>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!getTemp Bangalore`",
                            value="",
                            inline=False)

        if (command == "w!getatm" or command == "getatm"):
            embed.title = f"Command: `w!getAtm`"
            embed.description = "Displays the `pressure`, `humidity`, and `visibility` for the given city."
            embed.add_field(name="Syntax: `w!getAtm <city_name>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!getAtm Tokyo`",
                            value="", inline=False)

        if (command == "w!getweather" or command == "getweather"):
            embed.title = f"Command: `w!getWeather`"
            embed.description = "Displays the `weather` and `wind speed` for the given city."
            embed.add_field(name="Syntax: `w!getWeather <city_name>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!getWeather Mumbai`",
                            value="",
                            inline=False)

        if (command == "w!get" or command == "get"):
            embed.title = f"Command: `w!get`"
            embed.description = "Displays specific weather information for the given city. Specify one or more fields (upto 12) to get specific information (e.g., temperature, humidity, wind speed, etc.).\nIf you have only entered 1 field, add a comma after that attribute"
            embed.add_field(name="Syntax: `w!get <city_name> <field1, field2, ...>`",
                            value="",
                            inline=False)
            embed.add_field(
                name="Example 1: `w!get Los Angeles timezone, current temperature/current, forecast, humidity, weather`\n\nExample 2: `w!get Los Angeles humidity,`",
                value="",
                inline=False)

        if (command == "w!convert" or command == "convert"):
            embed.title = f"Command: `w!convert`"
            embed.description = "Converts the temperature unit to Celsius (c), Fahrenheit (f), or Kelvin (k)."
            embed.add_field(name="Syntax: `w!convert <unit>`",
                            value="",
                            inline=False)
            embed.add_field(name="Example: `w!convert f` or `w!convert farenheit`",
                            value="",
                            inline=False)

        await message.channel.send(embed=embed)
        return

    if (mes.split()[0] == "w!convert"):
        if (mes.split()[1] == "c" or mes.split()[1] == "celcius"):
            tempUnit = "c"
            await message.channel.send("Temperature unit has been set to Celsius")
        elif (mes.split()[1] == "f" or mes.split()[1] == "farenheit"):
            tempUnit = "f"
            await message.channel.send("Temperature unit has been set to Fahrenheit")
        elif (mes.split()[1] == "k" or mes.split()[1] == "kelvin"):
            tempUnit = "k"
            await message.channel.send("Temperature unit has been set to Kelvin")
        else:
            await message.channel.send("Please enter a valid unit (c/f/k)")
        return

    if (mes.split()[0] == "w!test"):
        await message.channel.send("Your test works")
        return

    if (mes.split()[0] == "w!getall"):
        city = mes.split("w!getall")[1]
        if (city != ""):
            try:
                embed = getAll(city)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Please give a valid/existing city name")
        else:
            await message.channel.send("Please give a valid/existing city name")
        return

    if (mes.split()[0] == "w!get"):
        spli = mes.split("w!get")
        rem = spli[1].strip()
        print(type(rem))
        attributes = []
        try:
            comma = rem.index(",")
            for i in range(comma, 0, -1):
                if rem[i] == " ":
                    city = rem[0:i]
                    attributes = rem[i+1:]
                    break
        except:
            city = rem
        if (city != ""):
            try:
                embed = get(city, attributes)
                await message.channel.send(embed=embed)
            except:
                if (attributes != [] and wrongCity == 1):
                    await message.channel.send("Please give a valid/existing city name")
                if (attributes == [] and wrongCity == 1):
                    await message.channel.send("Firstly, give a valid/existing city name. Secondly, specify some attributes. If you dont get how the command works then use `w!command get`")
                if (attributes == [] and wrongCity == 0):
                    await message.channel.send(f"Was it not clear that you're supposed to specify some attributes for {city}")
        else:
            if (attributes == [] and wrongCity == 0):
                await message.channel.send(f"Was it not clear that you're supposed to specify some attributes for {city}")
            if (attributes != [] and wrongCity == 1):
                await message.channel.send("Please give a valid/existing city name")
            if (attributes == [] and wrongCity == 1):
                await message.channel.send("Firstly, give a valid/existing city name. Secondly, specify some attributes. If you dont get how the command works then use `w!command get`")
        return

    if (mes.split()[0] == "w!getloc"):
        city = mes.split("w!getloc")[1]
        if (city != ""):
            try:
                embed = getLoc(city)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Please give a valid/existing city name")
        else:
            await message.channel.send("Please give a valid/existing city name")
        return

    if (mes.split()[0] == "w!gettemp"):
        city = mes.split("w!gettemp")[1]
        if (city != ""):
            try:
                embed = getTemp(city)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Please give a valid/existing city name")
        else:
            await message.channel.send("Please give a valid/existing city name")
        return

    if (mes.split()[0] == "w!getatm"):
        city = mes.split("w!getatm")[1]
        if (city != ""):
            try:
                embed = getAtm(city)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Please give a valid/existing city name")
        else:
            await message.channel.send("Please give a valid/existing city name")
        return

    if (mes.split()[0] == "w!getweather"):
        city = mes.split("w!getweather")[1]
        if (city != ""):
            try:
                embed = getWeather(city)
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Please give a valid/existing city name")
        else:
            await message.channel.send("Please give a valid/existing city name")
        return

    if (mes.split()[0][:2] == "w!"):
        await message.channel.send("Please enter a valid command")
        return

client.run("")
