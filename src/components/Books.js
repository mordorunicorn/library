import React from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/styles';
import {
  Badge,
  Card,
  CircularProgress,
  FormControlLabel,
  Grid,
  Hidden,
  Switch,
  TextField,
} from '@material-ui/core';

const useStyles = makeStyles(() => ({
  bookBox: {
    backgroundColor: '#f6f6f6',
    width: '100%',
    height: '100%',
    color: '#000000',
    overflowY: 'auto',
  },
  bookCover: {
    maxHeight: '150px',
    maxWidth: '100%',
  },
  defaultCover: {
    color: '#0066e2',
  },
  imgContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loadingBox: {
    backgroundColor: '#f6f6f6',
    width: '100%',
    height: '100%',
    color: '#000000',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
}));

const sortBooks = (bookList) => {
  return bookList.sort((bookA, bookB) => {
    return bookA.display_title.toLowerCase() > bookB.display_title.toLowerCase() ? 1 : -1;
  });
};

const BookCover = ({ book }) => {
  const classes = useStyles();
  const showChildrenBadge = !book.read && book.age_group === 'children';

  return (
    <Grid container item xs={4} sm={2} md={1}>
      <a href={'/#/books/' + book.id} style={{ textDecoration: "none" }}>
        {book.is_reading_challenge_eligible ?
          <Badge badgeContent="unread" color="primary" invisible={ book.read }>
            <Grid item xs={12} className={classes.imgContainer}>
              <>
                {book.cover_url ?
                  <img src={book.cover_url} className={classes.bookCover} alt="" /> :
                  <h3 className={classes.defaultCover}>{book.title}</h3>
                }
              </>
            </Grid>
          </Badge>
        :
          <Badge badgeContent="unread" color="secondary" invisible={ !showChildrenBadge }>
            <Grid item xs={12} className={classes.imgContainer}>
              <>
                {book.cover_url ?
                  <img src={book.cover_url} className={classes.bookCover} alt="" /> :
                  <h3 className={classes.defaultCover}>{book.title}</h3>
                }
              </>
            </Grid>
          </Badge>
        }
      </a>
    </Grid>
  );
};

const BookDetail = ({ book }) => {
  const classes = useStyles();

  return (
    <Grid item xs={4} sm={2} md={6} style={{ height: 250}}>
      <a href={'/#/books/' + book.id} style={{ textDecoration: 'none' }}>
        <Card className={classes.bookBox}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3} className={classes.imgContainer}>
              {book.cover_url ?
                <img src={book.cover_url} className={classes.bookCover} alt="" /> :
                <h3 className={classes.defaultCover}>{book.title}</h3>
              }
            </Grid>
            <Grid item container md={9}>
              <Grid item xs={12}>
                <h3>{book.title}</h3>
              </Grid>
              <Grid item xs={12}>
                <p>
                  <strong>Author: </strong>
                  {book.authors.map(author => `${author.first_name}${author.first_name ? " " : ""}${author.last_name}`).join(", ")}
                </p>
              </Grid>
              <Grid item xs={6}>
                <p>
                  <strong>Genre: </strong>
                  {book.subgenre.genre.name} > {book.subgenre.name}
                </p>
              </Grid>
              <Grid item xs={6}>
                {book.series &&
                  <p>
                    <strong>Series: </strong>
                    {book.series.name}
                  </p>
                }
              </Grid>
              <Grid item xs={6}>
                <p>
                  <strong>Tags: </strong>
                  {book.tags.map(tag => tag.name).join(", ")}
                </p>
              </Grid>
              <Grid item xs={6}>
                {book.read || <p>[Unread]</p>}
              </Grid>
            </Grid>
          </Grid>
        </Card>
      </a>
    </Grid>
  );
};

const Books = () => {
  const classes = useStyles();
  const [books, setBooks] = React.useState([]);
  const [booksLoaded, setBooksLoaded] = React.useState(false);
  const [filteredBooks, setFilteredBooks] = React.useState(sortBooks(books));
  const [onlyCovers, setOnlyCovers] = React.useState(true);
  const [showReadingChallenge, setShowReadingChallenge] = React.useState(false);
  const [showUnread, setShowUnread] = React.useState(false);

  const fetchBookList = async () => {
    let response = await axios.get('/api/books/');
    let json = await response.data;;
    return { success: true, data: json};
  }

  React.useEffect(() => {
    (async () => {
      let bookResponse = await fetchBookList();
      if (bookResponse.success) {
        setBooks(sortBooks(bookResponse.data));
        setBooksLoaded(true);
        setFilteredBooks(sortBooks(bookResponse.data))
      }
    })()
  }, []);

  const filterBooks = (books, challenge, unread) => {
    if (challenge) {
      books = books.filter(book => book.is_reading_challenge_eligible)
    }

    if (unread) {
      books = books.filter(book => book.is_reading_challenge_eligible && !book.read)
    }

    return books
  };

  const handleCoverChange = (e) => {
    setOnlyCovers(e.target.checked);
  };

  const handleReadingChallengeChange = (e) => {
    setShowReadingChallenge(e.target.checked);
    if (e.target.checked) {
      setFilteredBooks(filteredBooks.filter(book => book.is_reading_challenge_eligible))
    } else {
      setFilteredBooks(filterBooks(books, false, showUnread))
    }
  };

  const handleUnreadChange = (e) => {
    setShowUnread(e.target.checked);
    if (e.target.checked) {
      setFilteredBooks(filteredBooks.filter(book => book.is_reading_challenge_eligible && !book.read))
    } else {
      setFilteredBooks(filterBooks(books, showReadingChallenge, false))
    }
  };

  const search = (e) => {
    if (e.target.value) {
      setFilteredBooks(
        sortBooks(
          filterBooks(books, showReadingChallenge, showUnread).filter((book) =>
            book.title.toLowerCase().includes(e.target.value.toLowerCase())
          )
        )
      );
    } else {
      setFilteredBooks(filterBooks(books, showReadingChallenge, showUnread))
    }
  };

  return (
    <Grid container spacing={3} style={{ margin: 0, width: '100%' }}>
      {!booksLoaded ?
        <Card className={classes.loadingBox}>
          <CircularProgress />
        </Card> :
        <>
          <Grid container item xs={12}>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Search"
                onChange={search}
                margin="normal"
                variant="outlined"
                style={{ width: '100%' }}
              />
            </Grid>
            <Grid
              item
              xs={12}
              sm={2}
              style={{
                textAlign: 'center',
                display: 'flex',
                justifyContent: 'center',
              }}
            >
              <Hidden only={['xs', 'sm']}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={onlyCovers}
                      onChange={handleCoverChange}
                      color="primary"
                      name="onlyCovers"
                      inputProps={{ 'aria-label': 'primary checkbox' }}
                    />
                  }
                  label="Show Covers Only"
                />
              </Hidden>
            </Grid>
            <Grid
              item
              xs={12}
              sm={2}
              style={{
                textAlign: 'center',
                display: 'flex',
                justifyContent: 'center',
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={showUnread}
                    onChange={handleUnreadChange}
                    color="primary"
                    name="showUnread"
                    inputProps={{ 'aria-label': 'primary checkbox' }}
                  />
                }
                label="Show Unread Only"
              />
            </Grid>
            <Grid
              item
              xs={12}
              sm={2}
              style={{
                textAlign: 'center',
                display: 'flex',
                justifyContent: 'center',
              }}
            >
              <FormControlLabel
                control={
                  <Switch
                    checked={showReadingChallenge}
                    onChange={handleReadingChallengeChange}
                    color="primary"
                    name="showUnread"
                    inputProps={{ 'aria-label': 'primary checkbox' }}
                  />
                }
                label="Show Challenge Only"
              />
            </Grid>
          </Grid>
          {filteredBooks.map((book) =>
            onlyCovers ? (
              <BookCover key={book.id} book={book} />
            ) : (
              <BookDetail key={book.id} book={book} />
            )
          )}
        </>
      }
    </Grid>
  );
};

export default Books;
