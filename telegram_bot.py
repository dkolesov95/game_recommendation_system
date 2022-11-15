import pandas as pd
from difflib import SequenceMatcher
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TOKEN = 'YOUR TOKEN'

with open('cosine_similarity.pkl', 'rb') as f:
    cosine_similarity = pd.read_pickle(f)

with open('unique_game_cards.csv') as f:
    unique_game_cards = pd.read_csv(f, encoding='unicode_escape')


def start(update, context):
    update.message.reply_text('Hi! This bot can recommend games to you based on your ' \
                              'preferences. Send me the name of the game and see what you get.')


def check_name(text):
    ratio = unique_game_cards['name'].apply(lambda x: SequenceMatcher(None, text.lower(), x.lower()).ratio())
    best_match = ratio.sort_values(ascending=False).index[0]
    return unique_game_cards.loc[best_match]['name']


def get_recomendation(game_name):
    sim_scores = list(enumerate(cosine_similarity.loc[game_name]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    games = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]
    df = unique_game_cards.iloc[games].copy()
    df['scores'] = scores
    return df


def harmonic_mean(dataframe):
    ms_normalize = dataframe['metascore'] / max(unique_game_cards['metascore'])
    us_normalize = dataframe['userscore'] / max(unique_game_cards['userscore'])
    cosine_sim = dataframe['scores']
    return 3 / (1 / ms_normalize + 1 / us_normalize + 1 / cosine_sim)


def generate_message(game_name, recomendation_df):
    message = f"Do you mean <b>{game_name}</b>? If not, I recommend copying the " \
              f"name of the game from <a href='https://metacritic.com'>Metacritic</a>.\n\n"
    for index, (_, row) in enumerate(recomendation_df.iterrows()):
        har_mean = round(row['harmonic_mean'], 4)
        message += f"{index + 1}. <a href='https://metacritic.com{row['href']}'>{row['name']}</a> ({har_mean})\n"
    return message


def echo(update, context):
    game_name = check_name(update.message.text)
    recomendation_df = get_recomendation(game_name)
    recomendation_df['harmonic_mean'] = harmonic_mean(recomendation_df)
    recomendation_df.sort_values('harmonic_mean', ascending=False, inplace=True)
    message = generate_message(game_name, recomendation_df)
    update.message.reply_text(message, parse_mode='HTML', disable_web_page_preview=True)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
