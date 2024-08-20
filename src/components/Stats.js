import React from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/styles';
import {
  Box,
  Card,
  CircularProgress,
  Grid,
  Typography,
} from '@material-ui/core';

const useStyles = makeStyles(() => ({
  bookBox: {
    backgroundColor: '#f6f6f6',
    width: '100%',
    height: '100%',
    color: '#000000',
  },
  graphBox: {
    backgroundColor: '#f6f6f6',
    width: '100%',
    color: '#000000',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: 'none',
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
  title: {
    marginTop: '0.35em',
    marginLeft: '5%',
    display: 'flex',
    justifyContent: 'center',
  },
}));

function CircularProgressWithLabel(props) {
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
      <CircularProgress variant="determinate" style={{height: '100px', width: '100px'}} {...props} />
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          right: 0,
          position: 'absolute',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Typography variant="h5" component="div">
          {`${Math.round(props.value)}%`}
        </Typography>
      </Box>
    </Box>
  );
}

const Stats = () => {
  const classes = useStyles();
  const [stats, setStats] = React.useState({});
  const [statsLoaded, setStatsLoaded] = React.useState(false);
  const [readingChallengeProgress, setReadingChallengeProgress] = React.useState(0);

  const fetchStats = async () => {
    let response = await axios.get('/api/stats/');
    let json = await response.data;;
    return { success: true, data: json};
  }

  React.useEffect(() => {
    (async () => {
      let statsResponse = await fetchStats();
      if (statsResponse.success) {
        var stats_data = statsResponse.data;
        setStats(statsResponse.data);
        setStatsLoaded(true);
        setReadingChallengeProgress((stats_data.books_by_read_status.read*100)/(stats_data.books_by_read_status.read + stats_data.books_by_read_status.unread));
      }
    })()
  }, []);

  return (
    <Grid container spacing={3} style={{ margin: 0, width: '100%' }}>
      {!statsLoaded ?
        <Card className={classes.loadingBox}>
          <CircularProgress />
        </Card> :
        <>
          <Grid item md={4} style={{ height: 250}}>
            <Card className={classes.bookBox}>
              <Typography variant="h3" gutterBottom className={classes.title}>
                Books
              </Typography>
              <Typography variant="h4" gutterBottom className={classes.title}>
                {stats.book_count}
              </Typography>
            </Card>
          </Grid>
          <Grid item md={4} style={{ height: 250}}>
            <Card className={classes.bookBox}>
              <Typography variant="h3" gutterBottom className={classes.title}>
                Authors
              </Typography>
              <Typography variant="h4" gutterBottom className={classes.title}>
                {stats.author_count}
              </Typography>
            </Card>
          </Grid>
          <Grid item md={4} style={{ height: 250}}>
            <Card className={classes.bookBox}>
              <Typography variant="h3" gutterBottom className={classes.title}>
                Series
              </Typography>
              <Typography variant="h4" gutterBottom className={classes.title}>
                {stats.series_count}
              </Typography>
            </Card>
          </Grid>
          <Grid item md={4} style={{ height: 250}}>
            <Card className={classes.bookBox}>
              <Typography variant="h3" gutterBottom className={classes.title}>
                Reading Challenge
              </Typography>
              <Card className={classes.graphBox}>
                <CircularProgressWithLabel value={readingChallengeProgress} />
              </Card>
              <Typography variant="h5" gutterBottom className={classes.title}>
                {stats.books_by_read_status.read}/{stats.books_by_read_status.read + stats.books_by_read_status.unread}
              </Typography>
            </Card>
          </Grid>
        </>
      }
    </Grid>
  );
};

export default Stats;
