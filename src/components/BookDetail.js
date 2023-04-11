import React from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/styles';
import Card from '@material-ui/core/Card';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles(() => ({
  bookCover: {
    maxHeight: '150px',
    maxWidth: '100%',
    borderRadius: '5px',
  },
  imgContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
}));

const BookDetail = (props) => {
  const classes = useStyles();
  const defaultCover = 'https://cliparting.com/wp-content/uploads/2016/05/Book-clip-art-of-students-reading-clipart-2-image-8.png';

  const [book, setBook] = React.useState({});

  const fetchBook = async (book_id) => {
    let response = await axios.get(`/api/books/${book_id}/`);
    let json = await response.data;
    return { success: true, data: json};
  }

  React.useEffect(() => {
    (async () => {
      let bookResponse = await fetchBook(props.match.params.book_id);
      if (bookResponse.success) {
        setBook(bookResponse.data);
      }
    })()
  }, [props]);

  return (
    <Grid container spacing={3} style={{ padding: '10px' }}>
      <Card className={classes.bookBox}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={3} className={classes.imgContainer}>
            <img src={book.cover_url || defaultCover} className={classes.bookCover} alt="" />
          </Grid>
          <Grid item container md={9}>
            <Grid item xs={12}>
              <h3>{book.title}</h3>
            </Grid>
            <Grid item xs={12}>
              {book.authors && (
                <p>
                  <strong>Author: </strong>
                  {book.authors.map(author => `${author.first_name}${author.first_name ? " " : ""}${author.last_name}`).join(", ")}
                </p>
              )}
            </Grid>
            <Grid item xs={6}>
              <p>
                <strong>Genre: </strong>
                {book.subgenre && (
                  `${book.subgenre.genre.name} > ${book.subgenre.name}`
                )}
              </p>
              {book.read || <p>[Unread]</p>}
            </Grid>
            <Grid item xs={6}>
              {book.series && (
                <p>
                  <strong>Series: </strong>
                  {book.series.name}
                </p>
              )}
            </Grid>
          </Grid>
        </Grid>
      </Card>
    </Grid>
  );
};

export default BookDetail;
