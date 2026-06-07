<?php
/**
 * Quick test to verify Coptic date calculation
 * 
 * Expected results:
 * - Nov 24, 2025 = 15 Hatur 1742
 * - Nov 23, 2025 = 14 Hatur 1742
 * - Sep 11, 2025 = 1 Tut 1742
 */

// Simulate the conversion logic
function test_gregorian_to_coptic( $year, $month, $day ) {
    $is_leap = ( $year % 4 == 0 && ( $year % 100 != 0 || $year % 400 == 0 ) );
    
    $coptic_new_year_month = 9;
    $coptic_new_year_day = $is_leap ? 12 : 11;
    
    $current_date = mktime( 0, 0, 0, $month, $day, $year );
    $new_year_date = mktime( 0, 0, 0, $coptic_new_year_month, $coptic_new_year_day, $year );
    
    if ( $current_date >= $new_year_date ) {
        $coptic_year = $year - 283;
        $reference_new_year = $new_year_date;
    } else {
        $coptic_year = $year - 284;
        $prev_year = $year - 1;
        $prev_is_leap = ( $prev_year % 4 == 0 && ( $prev_year % 100 != 0 || $prev_year % 400 == 0 ) );
        $prev_new_year_day = $prev_is_leap ? 12 : 11;
        $reference_new_year = mktime( 0, 0, 0, 9, $prev_new_year_day, $prev_year );
    }
    
    $days_diff = (int) round( ( $current_date - $reference_new_year ) / 86400 );
    
    $coptic_month = min( 13, (int) floor( $days_diff / 30 ) + 1 );
    $coptic_day = ( $days_diff % 30 ) + 1;
    
    if ( $coptic_month > 12 ) {
        $coptic_month = 13;
        $coptic_day = $days_diff - 360 + 1;
    }
    
    $month_names = array(
        1 => 'Tut', 2 => 'Babah', 3 => 'Hatur', 4 => 'Kiyahk', 5 => 'Tubah', 6 => 'Amshir',
        7 => 'Baramhat', 8 => 'Baramudah', 9 => 'Bashans', 10 => 'Baunah', 11 => 'Abib', 12 => 'Misra', 13 => 'Nasie'
    );
    
    return array(
        'coptic_year' => $coptic_year,
        'coptic_month' => $coptic_month,
        'coptic_day' => $coptic_day,
        'month_name' => $month_names[$coptic_month],
        'days_diff' => $days_diff
    );
}

// Test cases
$tests = array(
    array( 2025, 11, 24, '15 Hatur 1742' ), // Nov 24, 2025
    array( 2025, 11, 23, '14 Hatur 1742' ), // Nov 23, 2025
    array( 2025, 9, 11, '1 Tut 1742' ),     // Sep 11, 2025 (Coptic New Year)
    array( 2025, 9, 10, '30 Misra 1741' ),  // Sep 10, 2025 (Last day of previous year)
);

echo "Coptic Date Conversion Tests:\n";
echo str_repeat( '=', 60 ) . "\n\n";

foreach ( $tests as $test ) {
    list( $year, $month, $day, $expected ) = $test;
    $result = test_gregorian_to_coptic( $year, $month, $day );
    $actual = $result['coptic_day'] . ' ' . $result['month_name'] . ' ' . $result['coptic_year'];
    $status = ( $actual === $expected ) ? '✓ PASS' : '✗ FAIL';
    
    printf(
        "%s | %04d-%02d-%02d => %s (days: %d)\n   Expected: %s\n\n",
        $status,
        $year, $month, $day,
        $actual,
        $result['days_diff'],
        $expected
    );
}
