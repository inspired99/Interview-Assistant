CREATE TYPE DIFFICULTY_LEVEL AS ENUM(
    'Easy',
    'Medium',
    'Hard'
);

CREATE TYPE STAGES AS ENUM(
    'Phone screen',
    'Online assessment',
    'Onsite'
);

CREATE TYPE COMPANY_NAME AS ENUM(
    'Google',
    'Microsoft',
    'Amazon',
    'Facebook',
    'Uber',
    'Airbnb'
);

CREATE TABLE Users(
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  
  UNIQUE (user_id)
);

CREATE TABLE UsersCompanies(
  user_id INT NOT NULL REFERENCES Users (user_id),
  company COMPANY_NAME NOT NULL,
  
  PRIMARY KEY (user_id, company)
);

CREATE TABLE UsersStages(
  user_id INT NOT NULL REFERENCES Users (user_id),
  stage STAGES NOT NULL,
  
  PRIMARY KEY (user_id, stage)
);

CREATE TABLE Tasks(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  examples TEXT NOT NULL,
  hints TEXT,
  constraints TEXT NOT NULL,
  difficulty DIFFICULTY_LEVEL NOT NULL,
  related_topics TEXT NOT NULL,
  company COMPANY_NAME NOT NULL,
  stage STAGES NOT NULL,
  link TEXT NOT NULL,
  
  UNIQUE (link)
);

CREATE TABLE Current(
  task_id INT NOT NULL REFERENCES Tasks (id),
  user_id INT NOT NULL REFERENCES Users (user_id),
  PRIMARY KEY (user_id)
);

CREATE TABLE Solved(
  task_id INT NOT NULL REFERENCES Tasks (id),
  user_id INT NOT NULL REFERENCES Users (user_id),
  PRIMARY KEY (task_id, user_id)
);

