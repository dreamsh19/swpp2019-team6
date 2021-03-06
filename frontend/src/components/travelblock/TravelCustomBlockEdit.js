import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import { blue } from '@material-ui/core/colors';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';

import clsx from 'clsx';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import TextField from '@material-ui/core/TextField';

import TravelBlockExpandButton from '../common/TravelBlockExpandButton';
import TimePickerWrapper from '../common/TimePicker';
import TravelBlockCloseButton from '../common/TravelBlockCloseButton';


const useCardStyles = makeStyles((theme) => ({
  card: {
    minWidth: 720,
    maxWidth: 720,
    '&:hover': {
      background: blue[50],
    },
  },
}));

const useTextStyles = makeStyles((theme) => ({
  description: {
    margin: 0,
    marginLeft: theme.spacing(1),
    width: 500,
  },
  title: {
    margin: theme.spacing(1),
    marginLeft: theme.spacing(2),
    width: 400,
  },
}));

export default function TravelCustomBlockEdit(props) {
  const cardClasses = useCardStyles();
  const textClasses = useTextStyles();
  const {
    items, index, handleRemove, handleBlockInfo,
  } = props;
  const {
    expand, description, time, startTime, endTime, title,
  } = items[index].info;

  const handleTime = (date) => {
    handleBlockInfo(index, 'time', date);
  };

  const handleStartTime = (date) => {
    handleBlockInfo(index, 'startTime', date);
  };

  const handleEndTime = (date) => {
    handleBlockInfo(index, 'endTime', date);
  };

  const handleTitle = (e) => {
    handleBlockInfo(index, 'title', e.target.value);
  };

  const removeHandler = () => {
    handleRemove(index);
  };

  const clickExpandHandler = () => {
    handleBlockInfo(index, 'expand', !expand);
  };

  const handleDescription = (e) => {
    handleBlockInfo(index, 'description', e.target.value);
  };

  return (
    <Card className={cardClasses.card}>
      <CardActions disableSpacing>
        {!expand
        && (
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <Grid container direction="row" justify="space-around" alignItems="center">
            <TimePickerWrapper
              label="Start Time"
              value={time}
              onChange={handleTime}
            />
          </Grid>
        </MuiPickersUtilsProvider>
        )}
        <Grid item>
          <TextField
            id="standard-multiline-flexible"
            label="Title"
            rowsMax="4"
            value={title}
            onChange={handleTitle}
            className={textClasses.title}
          />
        </Grid>
        <TravelBlockExpandButton expand={expand} clickExpandHandler={clickExpandHandler} />
        <TravelBlockCloseButton removeHandler={removeHandler} />
      </CardActions>
      <Collapse in={expand} timeout="auto" unmountOnExit>
        <CardContent>
          <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <Grid container direction="column" justify="space-around">
              <Grid container direction="row">
                <TimePickerWrapper
                  label="Start Time"
                  value={time}
                  onChange={handleTime}
                />
                {/* <TimePickerWrapper
                  label="End Time"
                  value={endTime}
                  onChange={handleEndTime}
                /> */}
              </Grid>
            </Grid>
          </MuiPickersUtilsProvider>
          <TextField
            id="standard-multiline-flexible"
            label="Description"
            multiline
            rowsMax="4"
            value={description}
            onChange={handleDescription}
            className={textClasses.description}
          />
        </CardContent>
      </Collapse>
    </Card>
  );
}
