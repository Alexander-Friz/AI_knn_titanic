import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Daten einlesen
df_train = pd.read_csv('titanic_training.csv')
df_test = pd.read_csv('titanic_test.csv')
df_test_with_survival = pd.read_csv('titanic_validate.csv')

# 2. Vorverarbeitung der Trainingsdaten
X_train = df_train.drop(['Survived', 'Cabin', 'Ticket', 'Name'], axis=1)
y_train = df_train['Survived']

X_train['Sex'] = X_train['Sex'].map({'male': 0, 'female': 1})
X_train['Embarked'] = X_train['Embarked'].map({'Q': 0, 'S': 1, 'C': 2})
X_train.dropna(inplace=True)
y_train = y_train[X_train.index]

# 3. Vorverarbeitung der Testdaten
X_test = df_test.drop(['Cabin', 'Ticket', 'Name'], axis=1)
X_test['Sex'] = X_test['Sex'].map({'male': 0, 'female': 1})
X_test['Embarked'] = X_test['Embarked'].map({'Q': 0, 'S': 1, 'C': 2})
X_test.fillna(X_train.mean(), inplace=True)  # Imputation von fehlenden Werten in den numerischen Spalten

# Auswahl der besten Features
best_features = ['Pclass', 'Sex', 'Parch', 'Embarked']
n_neighbors = 26  # Hier könnte man den besten n_neighbors Wert nutzen, den ihr gefunden habt #n = 26 --> Accuracy von 75,12% // statt standard n = 5 = 73%

# 4. Modell trainieren
knn = KNeighborsClassifier(n_neighbors=n_neighbors)
knn.fit(X_train[best_features], y_train)

# 5. Vorhersagen auf den Testdaten treffen
y_test_pred = knn.predict(X_test[best_features])

# 6. Vergleich mit den tatsächlichen Überlebensdaten
df_test_with_survival['Predicted_Survived'] = y_test_pred

# Anpassung: Wenn kein Mapping erfolgt, wird 'NIO' eingetragen
df_test_with_survival['Correct'] = df_test_with_survival.apply(
    lambda row: 'NIO' if pd.isna(row['Survived']) or pd.isna(row['Predicted_Survived']) else row['Survived'] == row['Predicted_Survived'],
    axis=1
)

# 7. Ergebnisse speichern
df_test_with_survival.to_csv('titanic_test_results.csv', index=False)

# Ausgabe der Ergebnisse
print("Ergebnisse gespeichert in 'titanic_test_results.csv'")

correct_predictions = df_test_with_survival['Correct'].apply(lambda x: x == True).sum()
total_predictions = len(df_test_with_survival)

accuracy = (correct_predictions / total_predictions)
