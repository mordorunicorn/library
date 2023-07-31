import React from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/styles';
import {
  Card,
  CircularProgress,
  Grid,
} from '@material-ui/core';

const useStyles = makeStyles(() => ({
  bookBox: {
    backgroundColor: '#f6f6f6',
    width: '100%',
    height: '100%',
    color: '#000000',
  },
  bookCover: {
    maxHeight: '150px',
    maxWidth: '100%',
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

const sortSeries = (seriesList) => {
  return seriesList.sort((seriesA, seriesB) => {
    return seriesA.name.toLowerCase() > seriesB.name.toLowerCase() ? 1 : -1;
  });
};

const SeriesDetail = ({ series }) => {
  const classes = useStyles();
  const defaultCover = 'https://cliparting.com/wp-content/uploads/2016/05/Book-clip-art-of-students-reading-clipart-2-image-8.png';

  return (
    <Grid item xs={4} sm={2} md={6} style={{ height: 250}}>
      <a href={'/#/series/' + series.id} style={{ textDecoration: 'none' }}>
        <Card className={classes.bookBox}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3} className={classes.imgContainer}>
              <img src={series.books[0].cover_url || defaultCover} className={classes.bookCover} alt="" />
            </Grid>
            <Grid item container md={9}>
              <Grid item xs={12}>
                <h3>{series.name}</h3>
              </Grid>
              <Grid item xs={12}>
                <p>
                  <strong>Author: </strong>
                  {series.authors.map(author => `${author.first_name}${author.first_name ? " " : ""}${author.last_name}`).join(", ")}
                </p>
              </Grid>
              <Grid item xs={6}>
                <p>
                  <strong>Books: </strong>
                  {series.books.length}
                </p>
              </Grid>
            </Grid>
          </Grid>
        </Card>
      </a>
    </Grid>
  );
};

const Series = () => {
  const classes = useStyles();
  const [series, setSeries] = React.useState([]);
  const [seriesLoaded, setSeriesLoaded] = React.useState(false);

  const fetchSeriesList = async () => {
    let response = await axios.get('/api/series/');
    let json = await response.data;;
    return { success: true, data: json};
  }

  React.useEffect(() => {
    (async () => {
      let seriesResponse = await fetchSeriesList();
      if (seriesResponse.success) {
        setSeries(sortSeries(seriesResponse.data));
        setSeriesLoaded(true);
      }
    })()
  }, []);

  return (
    <Grid container spacing={3} style={{ margin: 0, width: '100%' }}>
      {!seriesLoaded ?
        <Card className={classes.loadingBox}>
          <CircularProgress />
        </Card> :
        <>
          {series.map((series) =>
              <SeriesDetail key={series.id} series={series} />
            )
          }
        </>
      }
    </Grid>
  );
};

export default Series;
