
CREATE TABLE candidate_tweets
(
    user_name varchar(30),
    user_id varchar(255),
    created_date timestamp,
    tweet varchar(255)
);

create Table tweets
(
    user_name varchar(30),
    user_id varchar(255),
    created_date timestamp,
    tweet varchar(255)
);


CREATE TABLE retweets
(
    user_name varchar(30),
    user_id varchar(255),
    created_date timestamp,
    tweet varchar(255),
    original_tweet varchar(255),
    original_user_id varchar(255),
    original_user_name varchar(30)
);
