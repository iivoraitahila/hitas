from decimal import Decimal

# Depreciation multiplier static values
#
# FIXME: We haven't found a correct formula for this yet and haven't had enough time to check for it. Below
# is a table how this value approximately decreases but it's far from perfect.
#
# +-------------+----------------+--------------------------------------------------------+-----------|
# | timespan    | months         | formula                                                | accurate? |
# +-------------+----------------+--------------------------------------------------------+-----------|
# |   0-6 years |    1-72 months | always 1                                               | yes       |
# |  6-11 years |  73-133 months | ROUND(0.99979165^(<months>-72), 4)                     | yes       |
# | 11-16 years | 134-192 months | ROUND(<133 month value> * 0.9995825^(<months>-133), 4) | no        |
# | 16+ years   | 193+ months    | ROUND(<192 month value> * 0.9991665^(<months>-192), 4) | no        |
# +-------------+----------------+--------------------------------------------------------+-----------|
#
# It's hard to say if the values here are absolutely correct or not as these are hand-written to the old system and
# there might be mistakes in these values too.

_VALUES = [
    Decimal("0.9998"),
    Decimal("0.9996"),
    Decimal("0.9994"),
    Decimal("0.9992"),
    Decimal("0.999"),
    Decimal("0.9988"),
    Decimal("0.9985"),
    Decimal("0.9983"),
    Decimal("0.9981"),
    Decimal("0.9979"),
    Decimal("0.9977"),
    Decimal("0.9975"),
    Decimal("0.9973"),
    Decimal("0.9971"),
    Decimal("0.9969"),
    Decimal("0.9967"),
    Decimal("0.9965"),
    Decimal("0.9963"),
    Decimal("0.996"),
    Decimal("0.9958"),
    Decimal("0.9956"),
    Decimal("0.9954"),
    Decimal("0.9952"),
    Decimal("0.995"),
    Decimal("0.9948"),
    Decimal("0.9946"),
    Decimal("0.9944"),
    Decimal("0.9942"),
    Decimal("0.994"),
    Decimal("0.9938"),
    Decimal("0.9936"),
    Decimal("0.9934"),
    Decimal("0.9931"),
    Decimal("0.9929"),
    Decimal("0.9927"),
    Decimal("0.9925"),
    Decimal("0.9923"),
    Decimal("0.9921"),
    Decimal("0.9919"),
    Decimal("0.9917"),
    Decimal("0.9915"),
    Decimal("0.9913"),
    Decimal("0.9911"),
    Decimal("0.9909"),
    Decimal("0.9907"),
    Decimal("0.9905"),
    Decimal("0.9903"),
    Decimal("0.99"),
    Decimal("0.9898"),
    Decimal("0.9896"),
    Decimal("0.9894"),
    Decimal("0.9892"),
    Decimal("0.989"),
    Decimal("0.9888"),
    Decimal("0.9886"),
    Decimal("0.9884"),
    Decimal("0.9882"),
    Decimal("0.988"),
    Decimal("0.9878"),
    Decimal("0.9876"),
    Decimal("0.9872"),
    Decimal("0.9868"),
    Decimal("0.9863"),
    Decimal("0.9859"),
    Decimal("0.9855"),
    Decimal("0.9851"),
    Decimal("0.9847"),
    Decimal("0.9843"),
    Decimal("0.9839"),
    Decimal("0.9835"),
    Decimal("0.9831"),
    Decimal("0.9826"),
    Decimal("0.9822"),
    Decimal("0.9818"),
    Decimal("0.9814"),
    Decimal("0.981"),
    Decimal("0.9806"),
    Decimal("0.9802"),
    Decimal("0.9798"),
    Decimal("0.9794"),
    Decimal("0.979"),
    Decimal("0.9786"),
    Decimal("0.9782"),
    Decimal("0.9777"),
    Decimal("0.9773"),
    Decimal("0.9769"),
    Decimal("0.9765"),
    Decimal("0.9761"),
    Decimal("0.9757"),
    Decimal("0.9753"),
    Decimal("0.9749"),
    Decimal("0.9745"),
    Decimal("0.9741"),
    Decimal("0.9737"),
    Decimal("0.9733"),
    Decimal("0.9729"),
    Decimal("0.9725"),
    Decimal("0.9721"),
    Decimal("0.9717"),
    Decimal("0.9712"),
    Decimal("0.9708"),
    Decimal("0.9704"),
    Decimal("0.97"),
    Decimal("0.9696"),
    Decimal("0.9692"),
    Decimal("0.9688"),
    Decimal("0.9684"),
    Decimal("0.968"),
    Decimal("0.9676"),
    Decimal("0.9672"),
    Decimal("0.9668"),
    Decimal("0.9664"),
    Decimal("0.966"),
    Decimal("0.9656"),
    Decimal("0.9652"),
    Decimal("0.9648"),
    Decimal("0.9644"),
    Decimal("0.964"),
    Decimal("0.9636"),
    Decimal("0.9632"),
    Decimal("0.9624"),
    Decimal("0.9616"),
    Decimal("0.9608"),
    Decimal("0.96"),
    Decimal("0.9592"),
    Decimal("0.9584"),
    Decimal("0.9576"),
    Decimal("0.9568"),
    Decimal("0.956"),
    Decimal("0.9552"),
    Decimal("0.9544"),
    Decimal("0.9536"),
    Decimal("0.9528"),
    Decimal("0.952"),
    Decimal("0.9512"),
    Decimal("0.9504"),
    Decimal("0.9496"),
    Decimal("0.9488"),
    Decimal("0.9481"),
    Decimal("0.9473"),
    Decimal("0.9465"),
    Decimal("0.9457"),
    Decimal("0.9449"),
    Decimal("0.9441"),
    Decimal("0.9433"),
    Decimal("0.9425"),
    Decimal("0.9417"),
    Decimal("0.941"),
    Decimal("0.9402"),
    Decimal("0.9394"),
    Decimal("0.9386"),
    Decimal("0.9378"),
    Decimal("0.9371"),
    Decimal("0.9363"),
    Decimal("0.9355"),
    Decimal("0.9347"),
    Decimal("0.9339"),
    Decimal("0.9332"),
    Decimal("0.9324"),
    Decimal("0.9316"),
    Decimal("0.9308"),
    Decimal("0.93"),
    Decimal("0.9293"),
    Decimal("0.9285"),
    Decimal("0.9277"),
    Decimal("0.9269"),
    Decimal("0.9262"),
    Decimal("0.9254"),
    Decimal("0.9246"),
    Decimal("0.9239"),
    Decimal("0.9231"),
    Decimal("0.9223"),
    Decimal("0.9216"),
    Decimal("0.9208"),
    Decimal("0.92"),
    Decimal("0.9193"),
    Decimal("0.9185"),
    Decimal("0.9177"),
    Decimal("0.917"),
    Decimal("0.9162"),
    Decimal("0.9154"),
    Decimal("0.9147"),
    Decimal("0.9139"),
    Decimal("0.9131"),
    Decimal("0.9124"),
    Decimal("0.9116"),
    Decimal("0.9109"),
    Decimal("0.9101"),
    Decimal("0.9093"),
    Decimal("0.9086"),
    Decimal("0.9078"),
    Decimal("0.9071"),
    Decimal("0.9063"),
    Decimal("0.9056"),
    Decimal("0.9048"),
    Decimal("0.9041"),
    Decimal("0.9033"),
    Decimal("0.9025"),
    Decimal("0.9018"),
    Decimal("0.901"),
    Decimal("0.9003"),
    Decimal("0.8995"),
    Decimal("0.8988"),
    Decimal("0.898"),
    Decimal("0.8973"),
    Decimal("0.8965"),
    Decimal("0.8958"),
    Decimal("0.8951"),
    Decimal("0.8943"),
    Decimal("0.8936"),
    Decimal("0.8928"),
    Decimal("0.8921"),
    Decimal("0.8913"),
    Decimal("0.8906"),
    Decimal("0.8898"),
    Decimal("0.8891"),
    Decimal("0.8884"),
    Decimal("0.8876"),
    Decimal("0.8869"),
    Decimal("0.8861"),
    Decimal("0.8854"),
    Decimal("0.8847"),
    Decimal("0.8839"),
    Decimal("0.8832"),
    Decimal("0.8825"),
    Decimal("0.8817"),
    Decimal("0.881"),
    Decimal("0.8803"),
    Decimal("0.8795"),
    Decimal("0.8788"),
    Decimal("0.8781"),
    Decimal("0.8773"),
    Decimal("0.8766"),
    Decimal("0.8759"),
    Decimal("0.8751"),
    Decimal("0.8744"),
    Decimal("0.8737"),
    Decimal("0.8729"),
    Decimal("0.8722"),
    Decimal("0.8715"),
    Decimal("0.8708"),
    Decimal("0.87"),
    Decimal("0.8693"),
    Decimal("0.8686"),
    Decimal("0.8679"),
    Decimal("0.8671"),
    Decimal("0.8664"),
    Decimal("0.8657"),
    Decimal("0.865"),
    Decimal("0.8643"),
    Decimal("0.8635"),
    Decimal("0.8628"),
    Decimal("0.8621"),
    Decimal("0.8614"),
    Decimal("0.8607"),
    Decimal("0.8599"),
    Decimal("0.8592"),
    Decimal("0.8585"),
    Decimal("0.8578"),
    Decimal("0.8571"),
    Decimal("0.8564"),
    Decimal("0.8557"),
    Decimal("0.8549"),
    Decimal("0.8542"),
    Decimal("0.8535"),
    Decimal("0.8528"),
    Decimal("0.8521"),
    Decimal("0.8514"),
    Decimal("0.8507"),
    Decimal("0.85"),
    Decimal("0.8493"),
    Decimal("0.8486"),
    Decimal("0.8478"),
    Decimal("0.8471"),
    Decimal("0.8464"),
    Decimal("0.8457"),
    Decimal("0.845"),
    Decimal("0.8443"),
    Decimal("0.8436"),
    Decimal("0.8429"),
    Decimal("0.8422"),
    Decimal("0.8415"),
    Decimal("0.8408"),
    Decimal("0.8401"),
    Decimal("0.8394"),
    Decimal("0.8387"),
    Decimal("0.838"),
    Decimal("0.8373"),
    Decimal("0.8366"),
    Decimal("0.8359"),
    Decimal("0.8352"),
    Decimal("0.8345"),
    Decimal("0.8338"),
    Decimal("0.8331"),
    Decimal("0.8324"),
    Decimal("0.8317"),
    Decimal("0.831"),
    Decimal("0.8304"),
    Decimal("0.8297"),
    Decimal("0.829"),
    Decimal("0.8283"),
    Decimal("0.8276"),
    Decimal("0.8269"),
    Decimal("0.8262"),
    Decimal("0.8255"),
    Decimal("0.8248"),
    Decimal("0.8241"),
    Decimal("0.8234"),
    Decimal("0.8227"),
    Decimal("0.822"),
    Decimal("0.8213"),
    Decimal("0.8206"),
    Decimal("0.8199"),
    Decimal("0.8192"),
    Decimal("0.8185"),
    Decimal("0.8178"),
    Decimal("0.8171"),
    Decimal("0.8164"),
    Decimal("0.8157"),
    Decimal("0.815"),
    Decimal("0.8143"),
    Decimal("0.8136"),
    Decimal("0.8129"),
    Decimal("0.8122"),
    Decimal("0.8115"),
    Decimal("0.8108"),
    Decimal("0.8101"),
    Decimal("0.8094"),
    Decimal("0.8087"),
    Decimal("0.808"),
    Decimal("0.8073"),
    Decimal("0.8066"),
    Decimal("0.8059"),
    Decimal("0.8052"),
    Decimal("0.8045"),
    Decimal("0.8038"),
    Decimal("0.8031"),
    Decimal("0.8024"),
    Decimal("0.8017"),
    Decimal("0.801"),
    Decimal("0.8003"),
    Decimal("0.7996"),
    Decimal("0.7989"),
    Decimal("0.7982"),
    Decimal("0.7975"),
    Decimal("0.7968"),
    Decimal("0.7961"),
    Decimal("0.7954"),
    Decimal("0.7947"),
    Decimal("0.794"),
    Decimal("0.7933"),
    Decimal("0.7926"),
    Decimal("0.7919"),
    Decimal("0.7912"),
    Decimal("0.7905"),
    Decimal("0.7898"),
    Decimal("0.7891"),
    Decimal("0.7884"),
    Decimal("0.7877"),
    Decimal("0.787"),
    Decimal("0.7863"),
    Decimal("0.7856"),
    Decimal("0.7849"),
    Decimal("0.7842"),
    Decimal("0.7835"),
    Decimal("0.7828"),
    Decimal("0.7821"),
    Decimal("0.7814"),
    Decimal("0.7807"),
    Decimal("0.78"),
    Decimal("0.7793"),
    Decimal("0.7786"),
    Decimal("0.7779"),
    Decimal("0.7772"),
    Decimal("0.7765"),
    Decimal("0.7758"),
    Decimal("0.7751"),
    Decimal("0.7744"),
    Decimal("0.7737"),
    Decimal("0.773"),
    Decimal("0.7723"),
    Decimal("0.7716"),
    Decimal("0.7709"),
    Decimal("0.7702"),
    Decimal("0.7695"),
    Decimal("0.7688"),
    Decimal("0.7681"),
    Decimal("0.7674"),
    Decimal("0.7667"),
    Decimal("0.766"),
    Decimal("0.7653"),
    Decimal("0.7646"),
    Decimal("0.7639"),
    Decimal("0.7632"),
    Decimal("0.7625"),
    Decimal("0.7618"),
    Decimal("0.7611"),
    Decimal("0.7604"),
    Decimal("0.7597"),
    Decimal("0.759"),
    Decimal("0.7583"),
    Decimal("0.7576"),
    Decimal("0.7569"),
    Decimal("0.7562"),
    Decimal("0.7555"),
    Decimal("0.7548"),
    Decimal("0.7541"),
    Decimal("0.7534"),
    Decimal("0.7525"),
    Decimal("0.7518"),
    Decimal("0.7511"),
    Decimal("0.7504"),
    Decimal("0.7497"),
    Decimal("0.749"),
    Decimal("0.7483"),
    Decimal("0.7476"),
    Decimal("0.7469"),
    Decimal("0.7462"),
    Decimal("0.7455"),
    Decimal("0.7448"),
    Decimal("0.7441"),
    Decimal("0.7434"),
]


def depreciation_multiplier(months: int) -> Decimal:
    global _VALUES

    # When months <= 6 years then the value is always 1
    if months <= 72:  # 6*12 == 6 years
        return Decimal(1)
    else:
        index = months - 72
        # If given months is greater than the hardcoded list then calculate the value based on the static decrement on
        # the last value in the list
        if index > len(_VALUES):
            val = _VALUES[-1] - (Decimal("0.0007") * (index - len(_VALUES)))
            # Don't return negative multipliers
            return max(Decimal(0), val)
        else:
            # Return a hardcoded value
            return _VALUES[index - 1]
