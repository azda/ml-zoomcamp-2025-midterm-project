import pandas as pd
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define features
categorical_cols = [
    'sex',      # 0 = female, 1 = male
    'cp',       # chest pain type (4 values)
    'fbs',      # fasting blood sugar > 120 mg/dl
    'restecg',  # resting electrocardiographic results (values 0,1,2)
    'exang',    # exercise induced angina
    'slope',    # ST depression
    'ca',       # number of major vessels (0-3) colored by flourosopy
    'thal'      # Thalassemia
]

numerical_cols = [
    'age',
    'trestbps', # resting blood pressure
    'chol',     # serum cholestoral in mg/dl
    'thalach',  # maximum heart rate achieved
    'oldpeak'   # ST depression induced by exercise relative to rest
]

# Load data
print("Loading data...")
df = pd.read_csv('heart.csv')

# Prepare column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Split data
print("Splitting data...")
df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

# Reset index
df_full_train = df_full_train.reset_index(drop=True)

# Extract target
y_full_train = df_full_train.target.values
del df_full_train['target']

# Prepare features
print("Preparing features...")
dv = DictVectorizer(sparse=False)
train_dict = df_full_train[categorical_cols + numerical_cols].to_dict(orient='records')
X_train = dv.fit_transform(train_dict)

# Train Random Forest with best parameters
print("Training Random Forest model...")
rf = RandomForestClassifier(
    n_estimators=75,
    max_depth=5,
    min_samples_leaf=3,
    random_state=1,
    n_jobs=-1
)
rf.fit(X_train, y_full_train)

print(f"Model trained successfully!")
print(f"Number of features: {X_train.shape[1]}")

# Save model and vectorizer
print("Saving model and vectorizer...")
with open('model.pkl', 'wb') as f:
    pickle.dump((dv, rf), f)

print("Model saved to 'model.pkl'")
