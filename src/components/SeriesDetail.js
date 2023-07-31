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
    paddingRight: '10px',
  },
}));

const sortBooks = (books) => {
  return books.sort((bookA, bookB) => {
    return bookA.series_num > bookB.series_num ? 1 : -1;
  });
};

const SeriesDetail = (props) => {
  const classes = useStyles();
  const defaultCover = 'https://cliparting.com/wp-content/uploads/2016/05/Book-clip-art-of-students-reading-clipart-2-image-8.png';

  const [series, setSeries] = React.useState({});

  const fetchSeries = async (series_id) => {
    let response = await axios.get(`/api/series/${series_id}/`);
    let json = await response.data;
    return { success: true, data: json};
  }

  React.useEffect(() => {
    (async () => {
      let seriesResponse = await fetchSeries(props.match.params.series_id);
      if (seriesResponse.success) {
        setSeries(seriesResponse.data);
      }
    })()
  }, [props]);

  return (
    <Grid container spacing={3} style={{ padding: '10px' }}>
      <Card style={{ padding: '10px' }}>
        <Grid container spacing={3}>
          <Grid item container md={9}>
            <Grid item xs={12}>
              <h3>{series.name}</h3>
            </Grid>
            <Grid item xs={12}>
              {series.authors && (
                <p>
                  <strong>Author: </strong>
                  {series.authors.map(author => `${author.first_name}${author.first_name ? " " : ""}${author.last_name}`).join(", ")}
                </p>
              )}
            </Grid>
            {series.books && sortBooks(series.books).map((book) => {
              return (
                <Grid item xs={12} md={3} key={book.id} className={classes.imgContainer}>
                  <img src={book.cover_url || defaultCover} className={classes.bookCover} alt="" />
                </Grid>
              )
            })}
          </Grid>
        </Grid>
      </Card>
    </Grid>
  );
};

export default SeriesDetail;
