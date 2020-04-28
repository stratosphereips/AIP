#!/bin/bash
echo "Hi"
read this_is_a_test

test='hi'

if [ "$this_is_a_test" = "$test" ]
then
	echo "Great"
fi
