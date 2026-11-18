import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv("creditcard.csv")
print(df.dtypes)
df.info()
print(df.describe(include="all"))
print(df.duplicated().sum())
print(df.isnull().sum())
print("Total missing Values:",df.isnull().sum().sum())
df=df.drop_duplicates()
if df.isnull().sum().sum() > 0:
    raise ValueError("Missing values found. Handle them before model training.")

if df["Class"].isnull().any():
    raise ValueError("Target column contains missing values.")
print("\nAfter duplicate removal:")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Missing values:", df.isnull().sum().sum())
print("\nClass distribution:")
print(df["Class"].value_counts())
print(df.columns.tolist())
print(len(df.columns))
print(df['Class'].unique())
print(df['Class'].value_counts())
print(df['Amount'].describe())
plt.boxplot(df['Amount'])
plt.title('Amount - Noisy Data')
plt.savefig('amount_outlier.png')
print("Graph Saved")
plt.close()
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import (classification_report,confusion_matrix,ConfusionMatrixDisplay,average_precision_score)
# Separate features and target
X = df.drop('Class', axis=1)
y = df['Class']

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Scale Amount and Time using training data only
scaler = StandardScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train[['Amount', 'Time']] = scaler.fit_transform(
    X_train[['Amount', 'Time']]
)

X_test[['Amount', 'Time']] = scaler.transform(
    X_test[['Amount', 'Time']]
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
ConfusionMatrixDisplay.from_predictions(y_test,y_pred)
plt.title("Fraud Detection - Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()
print("\nAverage Precision Score:")
print(average_precision_score(y_test, model.predict_proba(X_test)[:, 1]))

print("\nModel training completed.")
print("Final Model Done _Outliers scaled, not removed")
plt.figure()
sns.countplot(x='Class',data=df)
plt.title('Class Imbalance - 0:Normal vs 1:Fraud')
plt.savefig('class_imbalance.png')
print("Graph 2 Saved: class_imbalance.png")
plt.close()
plt.figure()
df_fraud = df[df['Class']==1]['Amount']
df_normal = df[df['Class']==0]['Amount']
plt.hist([df_normal,df_fraud], bins=50, label=['Normal','Fraud'])
plt.legend()
plt.title('Amount Distribution - Fraud vs Normal')
plt.savefig('amount_fraud_vs_normal.png')
print("Graph 3 Saved: amount_fraud_vs_normal.png")
plt.close()
plt.figure()
plt.scatter(df['Time'],df['Amount'],c=df['Class'],alpha=0.3,s=1)
plt.title('Time vs Amount - Fraud Pattern')
plt.xlabel('Time')
plt.ylabel('Amount')
plt.savefig('time_vs_amount.png')
print("Graph 4 Saved: time_vs_amount.png")
plt.close()
plt.figure()
importances = pd.Series(model.feature_importances_, index=X.columns)
importances.nlargest(10).plot(kind='barh')
plt.title('Top 10 Fraud Indicators')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.close()
print ("Graph 5 Saved: feature_importance.png")
import joblib
joblib.dump({"model":model,"scaler":scaler},"fraud_model.pkl")
print("\nAll Done - 6 Graphs + Model Saved")

df.to_csv("fraud_dashboard_data.csv",index=False)
print("PowerBI dataset exported successfully!")