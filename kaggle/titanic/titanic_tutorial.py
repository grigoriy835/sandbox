import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


train_data = pd.read_csv("data/train.csv")
train_data.head()

test_data = pd.read_csv("data/test.csv")
test_data.head()

women = train_data.loc[train_data.Sex == 'female']["Survived"]
rate_women = sum(women)/len(women)

print("% of women who survived:", rate_women)

men = train_data.loc[train_data.Sex == 'male']["Survived"]
rate_men = sum(men)/len(men)

print("% of men who survived:", rate_men)





from sklearn.ensemble import RandomForestClassifier


def map_fee_to_quantil(x):
    for n, sum in {4: 31, 3: 14.5, 2: 7.9, 1: 0}.items():
        if x >= sum:
            return int(n)
    return int(1)

# train_data = train_data.loc[train_data["SibSp"] < 8] #todo check if it good

train_data['cabin_section'] = train_data['Cabin'].map(lambda x: str(x)[0])
train_data['fee_quantil'] = train_data['Fare'].map(map_fee_to_quantil)

test_data['fee_quantil'] = test_data['Fare'].map(map_fee_to_quantil)
test_data['cabin_section'] = test_data['Cabin'].map(lambda x: str(x)[0])


features = ["Pclass", "Sex", "SibSp", "Parch", 'fee_quantil']

X_test = pd.get_dummies(test_data[features])
X = pd.get_dummies(train_data[features])
y = train_data["Survived"]

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X, y)

predictions = model.predict(X_test)

output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('my_submission.csv', index=False)
print("Your submission was successfully saved!")